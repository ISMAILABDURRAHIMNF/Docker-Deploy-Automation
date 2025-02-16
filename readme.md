# Dockerfile Generator

Hi, thanks for visiting my repo, this project is a automation program with Docker. This Dockerfile Generator is accessed through in console, but this project will always be developed to bring more features.

## 🔧 How to use with Virtual Environment

Clone this repo to ur computer

```bash
  git clone https://github.com/ISMAILABDURRAHIMNF/Dockerfile-Generator.git
```

Use your virtual environment and install all required modules using `pip install` on the console

```bash
  pip install reqirements.txt -r
```

Create the `.env` file in the same directory as `main.py` using this variable.

```bash
  DB_HOST=
  DB_NAME=
  DB_USER=
  DB_PASS=
  SECRET_KEY=
  DEPLOY_PATH=
```

Use the program by running `src/main.py`

```bash
  python src/main.py
```

## 🔧 How to use with Docker

Clone this repo to ur computer

```bash
  git clone https://github.com/ISMAILABDURRAHIMNF/Dockerfile-Generator.git
```

Build docker image

```bash
  docker build -t automation-deploy-docker .
```

Run docker container with environment variabel (DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME, DEPLOY_PATH, SECRET_KEY). Replace the 8080 with your custom port u want.

```bash
  docker container run -d -p 8080:5000 \
    -e DB_HOST= \
    -e DB_USERNAME= \
    -e DB_PASSWORD= \
    -e DB_NAME= \
    -e DEPLOY_PATH= \
    -e SECRET_KEY= \
    automation-deploy-docker
```

## ❗Warning !

Make sure u already have an OpenAI API key and save it in the `.env` file. Make sure ur docker is running!
