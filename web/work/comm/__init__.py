import asyncio
import logging

from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from flask_login import LoginManager
from flask_socketio import SocketIO


auth = HTTPBasicAuth()
db = SQLAlchemy()
scheduler = APScheduler()
# scheduler = FlaskAPScheduler()
login_manager = LoginManager()
socketio = SocketIO()

# VERSION = '1.0.0.20240111'


@auth.verify_password
def verify_password(username, password):
    if username == 'miaowa' and password == 'pass':
        return True
    return False
