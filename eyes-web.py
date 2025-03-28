import os
import sys
import getopt
import flask
import logging
import traceback

from typing import List, Dict, Tuple, Any
from importlib import metadata
from gevent.pywsgi import WSGIServer
# from geventwebsocket.handler import WebSocketHandler

from comm import VERSION, Logger, LOG_KV, LOG_IMPORTANT
from web.app_avatar import create_avatar_app
from web.app_chat import create_chat_app, run_chat_app

app_name = "Eyes-Web"
logger = Logger(app_name)


def print_help(message: str = None):
    print(f"{app_name} {VERSION} By EyesYoga")
    print("usage: python3 eyes-web.py -d <app_name>")
    print(" e.g.: python3 eyes-web.py -w app_avatar")
    if message:
        print(message)


def run_app(args: List[str], port=8090):
    app_name = args[0]
    if app_name == "app_avatar":
        try:
            run_app_avatar("0.0.0.0", port)
        except Exception as e:
            logger.error(e)
            print(traceback.format_exc())
    elif app_name == "app_chat":
        try:
            run_app_chat("0.0.0.0", port)
        except Exception as e:
            logger.error(e)
            print(traceback.format_exc())
    else:
        LOG_IMPORTANT(f"WebApp: {app_name} is Unknown !")


def run_wsgi_app(args: List[str], port=8090):
    app_name = args[0]
    if app_name == "app_avatar":
        try:
            run_wsig_app_avatar("0.0.0.0", port)
        except Exception as e:
            logger.error(e)
            print(traceback.format_exc())
    elif app_name == "app_chat":
        try:
            run_wsig_app_chat("0.0.0.0", port)
        except Exception as e:
            logger.error(e)
            print(traceback.format_exc())
    else:
        LOG_IMPORTANT(f"WebApp: {app_name} is Unknown !")


def run_app_avatar(host: str, port: int):
    os.environ["FLASK_APP"] = "app_avatar"
    os.environ["FLASK_ENV"] = "development"

    app = create_avatar_app()

    debug_mode = 1
    if debug_mode:
        print(' * DEBUG mode')
        app.run(host=host, port=port, debug=True,
                use_debugger=False, use_reloader=False)
    else:
        print(' * NON-DEBUG mode')
        app.run(host=host, port=port, debug=False)


def run_app_chat(host: str, port: int):
    os.environ["FLASK_APP"] = "app_chat"
    os.environ["FLASK_ENV"] = "development"

    app = create_chat_app()
    run_chat_app(app, host, port, socketio=False, debug_mode=True)


def run_wsig_app_avatar(host: str, port: int):
    try:
        app = create_avatar_app()
        # server = WSGIServer((host, port), app, handler_class=WebSocketHandler)
        server = WSGIServer((host, port), app)
        server.serve_forever()
    except Exception as e:
        logger.error(e)
        print(traceback.format_exc())


def run_wsig_app_chat(host: str, port: int):
    try:
        app = create_chat_app()
        # server = WSGIServer((host, port), app, handler_class=WebSocketHandler)
        server = WSGIServer((host, port), app)
        server.serve_forever()
    except Exception as e:
        logger.error(e)
        print(traceback.format_exc())


if __name__ == "__main__":
    for m in [flask]:
        LOG_KV(m.__name__, metadata.version('flask'))

    try:
        opts, args = getopt.getopt(sys.argv[1:], "dw")
    except getopt.GetoptError as e:
        print_help(e)
        sys.exit(2)

    if len(opts) == 0 or len(args) == 0:
        print_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-d':
            run_app(args)
        elif opt == '-w':
            run_wsgi_app(args)
