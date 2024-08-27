from flask import Blueprint, request, jsonify
from .deploy_docker import remove_dir, run_container, stop_container, remove_image, process

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
    app_name = request.form['app_name']
    stop_container(app_name)
    remove_image(app_name)
    remove_dir(app_name)
    return jsonify({'message': 'App deleted successfully'})

@main.route('/start', methods=['POST'])
def start():
    app_name = request.form['app_name']
    run_container(app_name)
    return jsonify({'message': 'App started successfully'})

@main.route('/stop', methods=['POST'])
def stop():
    app_name = request.form['app_name']
    stop_container(app_name)
    return jsonify({'message': 'App stopped successfully'})