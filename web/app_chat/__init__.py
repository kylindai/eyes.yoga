import json
import os
import atexit
import datetime
import logging

from flask import Flask, app, session, request, render_template
from flask_login import login_required, current_user
# from flask_sse import sse

from comm import LOG_KV, LOG_IMPORTANT
from web.work.comm import auth, db, scheduler, login_manager, socketio
from web.app_chat.work.bp import chat

APP_VERSION = '1.0.0'
APP_COPYRIGHT = '2024.03'
APP_AUTHOR = 'eyes.yoga@hotmail.com'


def create_app(config_file: str = None):
    # create app
    instance_path = os.path.abspath("./web/instance/app_chat")
    app = Flask(__name__,
                instance_path=instance_path,
                instance_relative_config=True)
    # app_context = app.app_context()
    # app_context.push()

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # setup logger
    setup_logger(app)

    # config setting
    app.config['SECRET_KEY'] = 'eyes.yoga'
    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)
    app.config['REDIS_URL'] = 'redis://localhost'
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

    # blueprint
    app.register_blueprint(chat.bp)
    # app.register_blueprint(sse, url_prefix='/stream')

    # scheduler
    # app.config |= job_config
    # scheduler.init_app(app)
    # scheduler.start()

    # login
    # login_manager.init_app(app)
    # login_manager.login_view = 'user.user_login'

    socketio.init_app(app)

    return app


def run_app(app, host: str, port: int, debug_mode=True):
    if debug_mode:
        print(' * DEBUG mode')
        # app.run(host=host, port=port, debug=True,
        #         use_debugger=False, use_reloader=False)
        socketio.run(app, host=host, port=port, debug=True, use_reloader=False)
    else:
        print(' * NON-DEBUG mode')
        # app.run(host=host, port=port, debug=False)
        socketio.run(app, host=host, port=port, debug=False)


@atexit.register
def exit_app():
    # if scheduler.state:
    #     scheduler.shutdown()
    pass


def setup_logger(app):
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    # app logger format
    for handler in app.logger.handlers:
        handler.setFormatter(formatter)

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


def app_about():
    return {
        "version": APP_VERSION,
        "copyright": APP_COPYRIGHT,
        "author": APP_AUTHOR
    }


def index():
    return render_template("index.html", about=app_about())
