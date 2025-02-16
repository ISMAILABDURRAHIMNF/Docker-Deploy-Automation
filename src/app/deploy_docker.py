"""Deploy docker function file"""

import os
import shutil
import docker
from .query import query_db

client = docker.from_env()

PATH = os.getenv('DEPLOY_PATH')

def count_docker_data():
    """Count docker data in database function"""

    docker_data = query_db('SELECT * FROM docker_data')
    total_docker_data = len(docker_data)
    return total_docker_data

def get_app_name(id_container):
    """Get app name based on id function"""

    app_name = query_db('SELECT name FROM container WHERE id = '\
                        '%s', (id_container,), one=True)['name']
    return app_name

def check_app_slot(app_name, dstport):
    """Check app name slot function"""

    result = query_db('SELECT name FROM container WHERE name = %s OR '\
                      'dstport = %s', (app_name, dstport), one=True)
    return result

def remove_dir(app_name):
    """Remove file function"""

    shutil.rmtree(f'{PATH}{app_name}')

def build_image(app_name, docker_data_id, id_user):
    """Build docker image function"""

    dockerfile = f"{PATH}{app_name}/Dockerfile"
    query_db('INSERT INTO docker_data (id, dockerfile, docker_image) VALUES '\
             '(%s, %s, %s)', (docker_data_id, dockerfile, app_name), one=True)
    query_db('INSERT INTO container (name, user_id, docker_data_id) VALUES '\
             '(%s, %s, %s)', (app_name, id_user, docker_data_id), one=True)
    client.images.build(path=f'{PATH}{app_name}/', tag=app_name)

def remove_image(app_name):
    """Remove docker image function"""

    client.images.remove(app_name)

def remove_container(app_name):
    """Remove container function"""

    client.containers.get(app_name).remove(force=True)

def run_container(app_name, srcport, dstport):
    """Create and start container function"""

    client.containers.run(image=app_name, ports={srcport:dstport}, detach=True, name=app_name)
    query_db("UPDATE container SET status = 'running', srcport = %s, dstport = %s '\
             'WHERE name = %s", (srcport, dstport, app_name), one=True)

def start_container(app_name):
    """Start containter function"""

    client.containers.get(app_name).start()

def stop_container(app_name):
    """Stop container function"""

    client.containers.get(app_name).stop()

def process(app_name, token, srcport, dstport):
    """Processing build image and run container function"""

    count = count_docker_data()
    docker_data_id = f"D{count+1}"
    id_user = query_db('SELECT id FROM akun WHERE login_token = %s', (token,), one=True)['id']
    build_image(app_name, docker_data_id, id_user)
    run_container(app_name, srcport, dstport)
