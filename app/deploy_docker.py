import shutil
import docker
from .query import query_db

client = docker.from_env()

PATH = 'D:/Mini Project/File_Deploy/Folder_'

def count_docker_data():
    docker_data = query_db('SELECT * FROM docker_data')
    total_docker_data = len(docker_data)
    return total_docker_data

def move_dir(app_name):
    shutil.move(PATH/app_name, f'/docker/{app_name}')

def remove_dir(app_name):
    shutil.rmtree(f'/docker/{app_name}')

def build_image(app_name, docker_data_id, id_user):
    query_db('INSERT INTO docker_data (id_docker_data, docker_image) VALUES (%s, %s)', (docker_data_id,  app_name), one=True)
    query_db('INSERT INTO container (user_id, docker_data_id) VALUES (%s, %s)', (id_user, docker_data_id), one=True)
    client.images.build(path=f'{PATH}{app_name}/', tag=app_name)

def remove_image(app_name):
    client.images.remove(app_name)

def run_container(app_name, port, id_user):
    client.containers.run(image=app_name, ports={port:port}, detach=True, name=app_name)
    query_db("UPDATE container SET name = %s, status = 'running' WHERE user_id = %s", (app_name, id_user), one=True)

def stop_container(app_name):
    container = client.containers.get(app_name)
    container.stop()

def process(app_name, token, port):
    count = count_docker_data()
    docker_data_id = f"D{count+1}"
    id_user = query_db('SELECT id FROM akun WHERE login_token = %s', (token,), one=True)['id']
    build_image(app_name, docker_data_id, id_user)
    run_container(app_name, port, id_user)