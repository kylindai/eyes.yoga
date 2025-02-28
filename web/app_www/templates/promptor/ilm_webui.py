import os
import cgi
import sys
import json
import urllib
import logging

from http.server import CGIHTTPRequestHandler, HTTPServer
from ilm_client import chat_with_image
from ilm_param import service_id, func_desc, custom_request

logging.basicConfig(level=logging.INFO)


class MyHandler(CGIHTTPRequestHandler):
    def do_GET(self):
        logging.info(f"Received GET request for: {self.path}")
        super().do_GET()

    def do_POST(self):
        logging.info(f"Received POST request for: {self.path}")
        # super().do_POST()

        content_type, pdict = cgi.parse_header(
            self.headers.get('content-type'))
        content_length = int(self.headers.get('Content-Length', 0))

        post_data = self.rfile.read(content_length)
        post_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
        print("Received POST data:", post_data)

        sys_message = post_data['sys_message'][0]
        user_message = post_data['user_message'][0]
        answer = chat_with_image(
            service_id, sys_message, user_message, None, custom_request)
        print("Received CyberMind data:", answer)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b'POST request processed.')


if __name__ == "__main__":
    PORT = int(sys.argv[1])
    server = HTTPServer(("", PORT), MyHandler)
    logging.info(f"Serving on port {PORT}")
    server.serve_forever()
