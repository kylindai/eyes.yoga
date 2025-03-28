import os
import json
import time
import gevent
import asyncio
import urllib.parse

from typing import Dict, List, Tuple
from werkzeug.security import check_password_hash

from flask import (
    app, g, current_app, Blueprint, Response, request, stream_with_context,
    render_template, send_from_directory, redirect, url_for
)
from flask_login import UserMixin, login_user, logout_user, login_required
from flask_socketio import SocketIO, emit
# from flask_sse import sse

from comm import Logger, LogLevel, LOG_IMPORTANT, LOG_KV, LOG_ERROR

from web.work.comm import db, login_manager, socketio
from web.app_avatar.work.comm.utils import build_result, result_success, result_failure

bp = Blueprint('chat', __name__)

logger = Logger("app_chat", log_level=LogLevel.DEBUG)


@bp.route('/socketio')
def chat_socketio():
    return render_template("chat/socketio.html")


@bp.route('/sse')
def chat_sse():
    sse_host = current_app.config.get('SSE_HOST')
    return render_template("chat/sse.html", sse_host=sse_host)


@bp.route('/send', methods=['POST'])
async def chat_send():
    result = build_result()

    return Response(json.dumps(result, indent=4, sort_keys=False, ensure_ascii=False),
                    mimetype='application/json')


@bp.route('/stream/chat', methods=['GET'])
def chat_stream():
    result = build_result()

    @stream_with_context
    def generate(id):
        client_id = request.args.get('client_id')
        try:
            with current_app.app_context():
                while True:
                    ts = int(time.time())
                    data = {'id': id, 'ts': ts}
                    yield f'id: {id}\nevent: greeting\ndata: {json.dumps(data)}\n\n'
                    gevent.sleep(1)
                    # if t > 10:
                    #     break
                    id += 1
        except GeneratorExit as e:
            logger.error(f"generator exit, client_id = {client_id}")

    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    return Response(generate(1), headers=headers, mimetype='text/event-stream')


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('server_response', {'data': 'Welcome to the WebSocket server!'})


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
