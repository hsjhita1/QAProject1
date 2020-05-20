#!/usr/bin/env bash

sudo apt update -y

sudo apt install python3 -y

sudo apt install python3-pip -y

sudo apt install python3-venv -y

python3 -m venv venv

source /var/lib/jenkins/workspace/flask-project/venv/bin/activate

pip3 install -r requirements.txt

gunicorn --workers=4 --bind=0.0.0.0:5000 app:app
#python3 /var/lib/jenkins/workspace/flask-project/app.py