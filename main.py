import shutil
import docker
from flask import Flask, request, jsonify
import mysql.connector

conn = mysql.connector.connect(
    host='',
    user='',
    password='',
    database=''
    )

cursor = conn.cursor()  

app = Flask(__name__)
client = docker.from_env()

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

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    query = f"SELECT * FROM users WHERE username = %s"

    cursor.execute(query, (username,))
    result = cursor.fetchone()  
    if username == result[username] and password == result[password]:
        return jsonify({'message': 'Login successful'})
    return jsonify({'message': 'Login failed'})

app.run(debug=True, host='127.0.0.1', port=8050)