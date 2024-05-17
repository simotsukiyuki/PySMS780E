#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from gevent import pywsgi
import Config

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'TEST TEST TEST'
    
if __name__ == "__main__":
    server = pywsgi.WSGIServer((Config.webserver_ip, Config.webserver_port),app)
    server.serve_forever()