import shutil
import docker
from .query import query_db

client = docker.from_env()

PATH = 'D:/Mini Project/File_Deploy/Folder_'

def move_dir(app_name):
    shutil.move(f'{PATH}{app_name}', f'/docker/{app_name}')

def remove_dir(app_name):
    shutil.rmtree(f'/docker/{app_name}')

def build_image(app_name,token):
    client.images.build(path=f'{PATH}{app_name}/', tag=app_name)
    query_db('UPDATE akun SET docker_image = %s WHERE login_token = %s', (app_name, token), one=True)

def remove_image(app_name):
    client.images.remove(app_name)

def run_container(app_name, token):
    container = client.containers.run(image=app_name, ports={5000:5000}, detach=True, name=app_name)
    query_db('UPDATE akun SET docker_container = %s WHERE login_token = %s', (container, token), one=True)

def stop_container(app_name):
    container = client.containers.get(app_name)
    container.stop()

def process(app_name, token):
    build_image(app_name, token)
    run_container(app_name, token)