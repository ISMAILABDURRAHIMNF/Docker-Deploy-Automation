"""Main handler route file"""

from flask import Blueprint, request, jsonify
import mysql.connector
from .deploy_docker import (
    remove_dir,
    stop_container,
    remove_image,
    get_app_name,
    remove_container,
    start_container
)
from .query import query_db

handler = Blueprint('handler', __name__)

@handler.route('/', methods=['GET'])
def index():
    """Generate message"""

    return jsonify({'message': 'Backend Docker Deploy Automation Standby!'})

@handler.route('/delete', methods=['POST'])
def delete():
    """Delete container, image and file function"""

    id_container = request.get_json().get('id')
    app_name = get_app_name(id_container)
    remove_container(app_name)
    remove_image(app_name)
    remove_dir(app_name)
    query_db('DELETE FROM container WHERE name = %s', (app_name,), one=True)
    query_db('DELETE FROM docker_data WHERE docker_image = %s', (app_name,), one=True)
    return jsonify({'message': 'App deleted successfully'})

@handler.route('/start_container', methods=['POST'])
def start():
    """Start container function"""

    id_container = request.get_json().get('id')
    print(id_container)
    app_name = get_app_name(id_container)
    start_container(app_name)
    query_db("UPDATE container SET status = 'running' WHERE id = %s", (id_container,), one=True)
    return jsonify({'message': 'App started successfully'})

@handler.route('/stop_container', methods=['POST'])
def stop():
    """Stop container function"""

    id_container = request.get_json().get('id')
    print(id_container)
    app_name = get_app_name(id_container)
    print(app_name)
    stop_container(app_name)
    query_db("UPDATE container SET status = 'stopped' WHERE id = %s", (id_container,), one=True)
    return jsonify({'message': 'App stopped successfully'})

@handler.route('/get_docker_data', methods=['POST'])
def check_image():
    """Get docker data from database function"""

    data = request.get_json()
    token = data.get('token')
    user_id = query_db('SELECT id FROM akun WHERE login_token = %s', (token,), one=True)['id']
    docker_data = query_db('SELECT id, name, status FROM container '\
                           'WHERE user_id = %s', (user_id,), one=False)
    print(docker_data)
    return jsonify({'docker_data': docker_data})

@handler.route('/tes_db', methods=['GET'])
def tes_db():
    """Database connection test function"""

    try:
        print("Starting database query...")
        query = 'desc akun;'
        result = query_db(query)
        print("Query result:", result)
        return jsonify({'message': 'tes_db', 'result': result})
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Error', 'error': str(e)}), 500
