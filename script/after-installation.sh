#!/bin/bash
source ~/.bashrc
printenv | sort
source /var/lib/jenkins/workspace/flask-project/venv/bin/activate
python3 /var/lib/jenkins/workspace/flask-project/app.py