import shutil
import docker

client = docker.from_env()

def move_dir(app_name):
    shutil.move(f'/uploads/{app_name}', f'/docker/{app_name}')

def build_image(app_name):
    client.images.build(path=f'/docker/{app_name}', tag=app_name)

def run_container(app_name):
    client.containers.run(app_name, detach=True)

def stop_container(app_name):
    container = client.containers.get(app_name)
    container.stop()

def main():
    app_name = 'my_app'
    move_dir(app_name)

if __name__ == '__main__':
    main()