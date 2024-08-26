import shutil
import docker
from flask import Flask, request, jsonify
import mysql.connector
from dotenv import load_dotenv
import os
import bcrypt

load_dotenv()
  
app = Flask(__name__)
client = docker.from_env()

def create_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

def query_db(query, args=(), one=False):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, args)
    result = cursor.fetchone() if one else cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def move_dir(app_name):
    shutil.move(f'/uploads/{app_name}', f'/docker/{app_name}')

def remove_dir(app_name):
    shutil.rmtree(f'/docker/{app_name}')

def build_image(app_name):
    client.images.build(path=f'/docker/{app_name}', tag=app_name)

def run_container(app_name):
    client.containers.run(app_name, detach=True)

def stop_container(app_name):
    container = client.containers.get(app_name)
    container.stop()

def process(app_name):
    move_dir(app_name)
    build_image(app_name)
    run_container(app_name)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Backend Docker Deploy Automation Standby!'})

@app.route('/deploy', methods=['POST'])
def deploy():
    app_name = request.form['app_name']
    process(app_name)
    return jsonify({'message': 'App deployed successfully'})

@app.route('/delete', methods=['POST'])
def delete():
    app_name = request.form['app_name']
    stop_container(app_name)
    client.images.remove(app_name)
    remove_dir(app_name)
    return jsonify({'message': 'App deleted successfully'})

@app.route('/start', methods=['POST'])
def start():
    app_name = request.form['app_name']
    run_container(app_name)
    return jsonify({'message': 'App started successfully'})

@app.route('/stop', methods=['POST'])
def stop():
    app_name = request.form['app_name']
    stop_container(app_name)
    return jsonify({'message': 'App stopped successfully'})

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    query_db('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
    
    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/login', methods=['GET','POST'])
def login():
    username = request.form['username'] 
    password = request.form['password']

    user = query_db('SELECT * FROM users WHERE username = %s', (username,), one=True)

    if user and bcrypt.checkpw(password.encode(), user['password'].encode('utf-8')):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
        
app.run(debug=True, port=8050)