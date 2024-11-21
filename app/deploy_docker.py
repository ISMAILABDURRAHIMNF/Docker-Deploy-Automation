import shutil
import docker
from .query import query_db

client = docker.from_env()

PATH = 'D:/Mini Project/File_Deploy/Folder_'

def count_docker_data():
    docker_data = query_db('SELECT * FROM docker_data')
    total_docker_data = len(docker_data)
    return total_docker_data

def get_app_name(id_container):
    app_name = query_db('SELECT name FROM container WHERE id = %s', (id_container,), one=True)['name']
    return app_name

def move_dir(app_name):
    shutil.move(PATH/app_name, f'/docker/{app_name}')

def remove_dir(app_name):
    shutil.rmtree(f'{PATH}{app_name}')

def build_image(app_name, docker_data_id, id_user):
    query_db('INSERT INTO docker_data (id, docker_image) VALUES (%s, %s)', (docker_data_id,  app_name), one=True)
    query_db('INSERT INTO container (name, user_id, docker_data_id) VALUES (%s, %s, %s)', (app_name, id_user, docker_data_id), one=True)
    client.images.build(path=f'{PATH}{app_name}/', tag=app_name)

def remove_image(app_name):
    client.images.remove(app_name)

def remove_container(app_name):
    client.containers.get(app_name).remove(force=True)

def run_container(app_name, port):
    client.containers.run(image=app_name, ports={port:port}, detach=True, name=app_name)
    query_db("UPDATE container SET status = 'running' WHERE name = %s", (app_name,), one=True)

def start_container(app_name):
    client.containers.get(app_name).start()

def stop_container(app_name):
    client.containers.get(app_name).stop()

def process(app_name, token, port):
    count = count_docker_data()
    docker_data_id = f"D{count+1}"
    id_user = query_db('SELECT id FROM akun WHERE login_token = %s', (token,), one=True)['id']
    build_image(app_name, docker_data_id, id_user)
    run_container(app_name, port)