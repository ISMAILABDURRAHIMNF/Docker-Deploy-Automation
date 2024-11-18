from flask import Blueprint, request, jsonify
from .deploy_docker import remove_dir, run_container, stop_container, remove_image, process
from .query import query_db
from .decorator import login_required

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Backend Docker Deploy Automation Standby!'})

@main.route('/deploy', methods=['POST'])
@login_required
def deploy():
    app_name = request.form['app_name']
    process(app_name)
    return jsonify({'message': 'App deployed successfully'})

@main.route('/delete', methods=['POST'])
@login_required
def delete():
    app_name = request.form['app_name']
    stop_container(app_name)
    remove_image(app_name)
    remove_dir(app_name)
    return jsonify({'message': 'App deleted successfully'})

@main.route('/start', methods=['POST'])
@login_required
def start():
    app_name = request.form['app_name']
    run_container(app_name)
    return jsonify({'message': 'App started successfully'})

@main.route('/stop', methods=['POST'])
@login_required
def stop():
    app_name = request.form['app_name']
    stop_container(app_name)
    return jsonify({'message': 'App stopped successfully'})

@main.route('/get_docker_data', methods=['POST'])
def check_image():
    data = request.get_json()
    token = data.get('token')
    user_id = query_db('SELECT id FROM akun WHERE login_token = %s', (token,), one=True)['id']
    docker_data = query_db('SELECT c.id_container, c.name, c.status, d.dockerfile FROM container c JOIN docker_data d ON c.docker_data_id=d.id_docker_data WHERE c.user_id = %s', (user_id,), one=False)
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
