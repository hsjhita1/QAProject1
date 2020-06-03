#!/bin/bash
sudo cp etc/systemd/system/flask.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable flask.service
source venv/bin/activate
pip3 install -r requirements.txt