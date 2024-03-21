import os
import json
import urllib.parse

from typing import Dict, List, Tuple
from werkzeug.security import check_password_hash

from flask import (
    app, g, current_app, Blueprint, render_template, Response, request, send_from_directory, redirect, url_for
)
from flask_login import UserMixin, login_user, logout_user, login_required


from comm import Logger, LOG_IMPORTANT, LOG_KV, LOG_ERROR
from web.work.comm import db, login_manager

bp = Blueprint('system', __name__)


@bp.route('/avatar')
def avatar():
    return render_template("avatar/index.html")


@bp.route('/avatar/test', methods=['GET'])
def avatar_test():
    return render_template('avatar/test.html')
