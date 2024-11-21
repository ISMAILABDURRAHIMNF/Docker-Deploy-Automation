from flask import Blueprint, request, jsonify
from .deploy_docker import remove_dir, stop_container, remove_image, process, get_app_name, remove_container, start_container
from .query import query_db

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Backend Docker Deploy Automation Standby!'})

@main.route('/deploy', methods=['POST'])
def deploy():
    app_name = request.form['app_name']
    process(app_name)
    return jsonify({'message': 'App deployed successfully'})

@main.route('/delete', methods=['POST'])
def delete():
    id_container = request.get_json().get('id')
    app_name = get_app_name(id_container)
    remove_container(app_name)
    remove_image(app_name)
    remove_dir(app_name)
    query_db('DELETE FROM container WHERE name = %s', (app_name,), one=True)
    query_db('DELETE FROM docker_data WHERE docker_image = %s', (app_name,), one=True)
    return jsonify({'message': 'App deleted successfully'})

@main.route('/start_container', methods=['POST'])
def start():
    id_container = request.get_json().get('id')
    print(id_container)
    app_name = get_app_name(id_container)
    start_container(app_name)
    query_db("UPDATE container SET status = 'running' WHERE id = %s", (id_container,), one=True)
    return jsonify({'message': 'App started successfully'})

@main.route('/stop_container', methods=['POST'])
def stop():
    id_container = request.get_json().get('id')
    print(id_container)
    app_name = get_app_name(id_container)
    print(app_name)
    stop_container(app_name)
    query_db("UPDATE container SET status = 'stopped' WHERE id = %s", (id_container,), one=True)
    return jsonify({'message': 'App stopped successfully'})

@main.route('/get_docker_data', methods=['POST'])
def check_image():
    data = request.get_json()
    token = data.get('token')
    user_id = query_db('SELECT id FROM akun WHERE login_token = %s', (token,), one=True)['id']
    docker_data = query_db('SELECT c.id, c.name, c.status, d.dockerfile FROM container c JOIN docker_data d ON c.docker_data_id=d.id WHERE c.user_id = %s', (user_id,), one=False)
    print(docker_data)
    return jsonify({'docker_data': docker_data})

@main.route('/tes_db', methods=['GET'])
def tes_db():
    try:
        print("Starting database query...")
        query = 'desc akun;'
        result = query_db(query)
        print("Query result:", result)
        return jsonify({'message': 'tes_db', 'result': result})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Error', 'error': str(e)}), 500
