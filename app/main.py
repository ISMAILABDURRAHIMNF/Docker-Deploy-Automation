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

@main.route('/tes_db', methods=['GET'])
def tes_db():
    query = 'SELECT * FROM user'
    result = query_db(query)
    return jsonify({'message': 'tes_db', 'result': result})