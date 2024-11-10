import shutil
import docker

client = docker.from_env()

PATH = 'D:/Mini Project/File_Deploy/'

def move_dir(app_name):
    shutil.move(f'{PATH}/{app_name}', f'/docker/{app_name}')

def remove_dir(app_name):
    shutil.rmtree(f'/docker/{app_name}')

def build_image(app_name):
    client.images.build(path=f'/docker/{app_name}', tag=app_name)

def remove_image(app_name):
    client.images.remove(app_name)

def run_container(app_name):
    client.containers.run(app_name, detach=True)

def stop_container(app_name):
    container = client.containers.get(app_name)
    container.stop()

def process(app_name):
    move_dir(app_name)
    build_image(app_name)
    run_container(app_name)