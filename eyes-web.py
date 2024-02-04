import os
import sys
import getopt
import flask
import logging
import traceback
import web.app_www as app_www

from typing import List, Dict, Tuple, Any
from importlib import metadata
from gevent.pywsgi import WSGIServer
# from geventwebsocket.handler import WebSocketHandler

from comm import VERSION, Logger, LOG_KV, LOG_IMPORTANT

app_name = "Eyes-Web"
logger = Logger(app_name)


def print_help(message: str = None):
    print(f"{app_name} {VERSION} By EyesYoga")
    print("usage: python3 eyes-web.py -d <app_name>")
    print(" e.g.: python3 eyes-web.py -w app_www")
    if message:
        print(message)


def run_app(args: List[str]):
    app_name = args[0]
    if app_name == "app_www":
        try:
            run_app_www("0.0.0.0", 8080)
        except Exception as e:
            logger.error(e)
    else:
        LOG_IMPORTANT(f"WebApp: {app_name} is Unknown !")


def run_wsgi_app(args: List[str]):
    app_name = args[0]
    if app_name == "app_www":
        try:
            run_wsig_app_www("0.0.0.0", 8080)
        except Exception as e:
            logger.error(e)
    else:
        LOG_IMPORTANT(f"WebApp: {app_name} is Unknown !")


def run_app_www(host: str, port: int):
    os.environ["FLASK_APP"] = "app_www"
    os.environ["FLASK_ENV"] = "development"

    app = app_www.create_app()
    # socketio = SocketIO(app)

    debug_mode = 1
    if debug_mode:
        print(' * DEBUG mode')
        app.run(host=host, port=port, debug=True,
                use_debugger=False, use_reloader=False)
        # socketio.run(app, host=host, port=port, debug=True, use_reloader=False)
    else:
        print(' * NON-DEBUG mode')
        app.run(host=host, port=port, debug=False)
        # socketio.run(app, host=host, port=port, debug=False)


def run_wsig_app_www(host: str, port: int):
    try:
        app = app_www.create_app()
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
