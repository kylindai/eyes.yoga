import os
import json
import urllib.parse

from typing import Dict, List, Tuple
from werkzeug.security import check_password_hash

from flask import (
    app, g, current_app, Blueprint, Response, request,
    render_template, send_from_directory, redirect, url_for
)
from flask_login import UserMixin, login_user, logout_user, login_required

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


@bp.route('/avatar/greeter', methods=['GET'])
def avatar_greeter():
    return render_template('avatar/greeter.html')


@bp.route('/avatar/chat', methods=['POST'])
def avatar_chat():
    result = build_result()
    return Response(json.dumps(result, indent=4, sort_keys=False, ensure_ascii=False),
                    mimetype='application/json')
