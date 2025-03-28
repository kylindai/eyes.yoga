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

bp = Blueprint('avatar', __name__)


@bp.route('/avatar')
def avatar():
    return render_template("avatar/index.html")


@bp.route('/avatar/test', methods=['GET'])
def avatar_test():
    return render_template('avatar/test.html')


@bp.route('/avatar/study', methods=['GET'])
def avatar_study():
    return render_template('avatar/study.html')


@bp.route('/avatar/greeter', methods=['GET'])
def avatar_greeter():
    sse_host = current_app.config['SSE_HOST']
    return render_template('avatar/greeter.html', sse_host=sse_host)


# @bp.route('/avatar/message')
# def avatar_message():
#     sse.publish({"message": f"Hello! {time.time()}"}, type='greeting')
#     return "Message sent!"
