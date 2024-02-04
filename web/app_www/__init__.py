import json
import os
import atexit
import datetime
import logging

from flask import Flask, app, session, request, render_template
from flask_login import login_required, current_user

from comm import LOG_KV, LOG_IMPORTANT
from web.work.comm import auth, db, scheduler, login_manager

APP_VERSION = '1.0.0'
APP_COPYRIGHT = '2024.02'
APP_AUTHOR = 'eyes.yoga@outlook.com'


def create_app(config_file: str = None):
    # create app
    instance_path = os.path.abspath("./web/instance/app_www")
    app = Flask(__name__,
                instance_path=instance_path,
                instance_relative_config=True)
    # app_context = app.app_context()
    # app_context.push()

    # setup logger
    setup_logger(app)

    # register exit
    atexit.register(exit_app)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    # app logger format
    for handler in app.logger.handlers:
        handler.setFormatter(formatter)

    # config setting
    app.config['SECRET_KEY'] = 'eyes.yoga'
    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)
    # app.config['DATA_PATH'] = os.path.abspath("./web/data/")

    # load config
    config_file = 'conf/config.json'
    app.config.from_file(config_file, json.load)

    # other config
    app.config['JSON_AS_ASCII'] = False

    # add jinja setting
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.globals.update(a=app_about)

    # init db
    # app.config |= db_config
    # db.init_app(app)

    # home index
    app.add_url_rule('/', endpoint='index', view_func=index)
    app.add_url_rule('/avatar', endpoint='avatar', view_func=avatar)
    app.add_url_rule('/prompt', endpoint='prompt', view_func=prompt)

    # blueprint
    # app.register_blueprint(user.bp)

    # scheduler
    # app.config |= job_config
    # scheduler.init_app(app)
    # scheduler.start()

    # login
    # login_manager.init_app(app)
    # login_manager.login_view = 'user.user_login'

    return app


def setup_logger(app):
    config_file = os.path.join(app.instance_path, f"conf/logging.ini")
    LOG_KV("logging_config", config_file)
    if os.path.exists(config_file):
        from logging import config
        config.fileConfig(config_file)

    # format = '%(asctime)s - %(levelname)s'
    # logger = logging.getLogger('root')
    # for handler in logger.handlers[:]:
    #     handler.setFormatter(logging.Formatter(format))

    # logger = logging.getLogger('werkzeug')
    # logger.propagate = False
    # logger.disabled = True


def exit_app():
    # if scheduler.state:
    #     scheduler.shutdown()
    pass


def app_about():
    return {
        "version": APP_VERSION,
        "copyright": APP_COPYRIGHT,
        "author": APP_AUTHOR
    }


def index():
    return render_template("index.html", about=app_about())


def avatar():
    return render_template("avatar/avatar.html")


def prompt():
    # just for test
    version = request.args.get('v')
    if version == '2':
        return render_template(f"promptor/prompt{version}.html")
    else:
        return render_template("promptor/prompt.html")
