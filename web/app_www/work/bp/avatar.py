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
from flask_sse import sse

from comm import Logger, LOG_IMPORTANT, LOG_KV, LOG_ERROR

from web.work.comm import db, login_manager
from web.app_www.work.comm.utils import build_result, result_success, result_failure

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
    return render_template('avatar/greeter.html')


@bp.route('/avatar/chat', methods=['GET'])
def avatar_chat():
    result = build_result()

    def generate(t):
        id = int(time.time())
        while True:
            data = {'id': id, 'ts': t}
            yield f'id: {id}\nevent: greeting\ndata: {json.dumps(data)}\n\n'
            time.sleep(1)
            if t > 10:
                break
            t += 1

    return Response(generate(1), mimetype='text/event-stream')


@bp.route('/avatar/message')
def avatar_message():
    sse.publish({"message": f"Hello! {time.time()}"}, type='greeting')
    return "Message sent!"
