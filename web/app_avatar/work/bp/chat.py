import os
import json
import time
import urllib.parse

from typing import Dict, List, Tuple
from werkzeug.security import check_password_hash

from flask import (
    app, g, current_app, Blueprint, Response, request,
    render_template, send_from_directory, redirect, url_for
)
from flask_login import UserMixin, login_user, logout_user, login_required
from flask_socketio import SocketIO, emit
# from flask_sse import sse

from comm import Logger, LOG_IMPORTANT, LOG_KV, LOG_ERROR

from web.work.comm import db, login_manager, socketio
from web.app_avatar.work.comm.utils import build_result, result_success, result_failure

bp = Blueprint('chat', __name__)


@bp.route('/chat')
def avatar():
    return render_template("chat/index.html")


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('server_response', {'data': 'Welcome to the WebSocket server!'})


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
