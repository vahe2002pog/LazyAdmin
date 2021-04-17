from os import path
from functools import wraps
from flask import (abort, jsonify, make_response, redirect, render_template,
                   request, send_from_directory, url_for, Markup, Response)
import random
import math
import os
import re
import datetime
import jwt


from app import app

from app.classes.video import Video
from app.config import service_token, secure_key, app_id, website_address, JWT_SECRET

import requests
import json

user_cache = dict()
user_cache_stack = []

def auth_check(token):
    response = requests.get(
        'https://api.vk.com/method/secure.checkToken?token={0}&client_secret={1}&access_token={2}&v=5.126'.format(
            token, secure_key, service_token))
    if response.json().get('response') != None:
        return {'valid': True, 'user_id': response.json().get('response').get('user_id')}
    else:
        return {'valid': False}

def answer_template(data=None, error=None, meta=None):
    answer = {
        'data': data,
        'error': error,
        'meta': meta
    }
    return json.dumps(answer)

def use_guard(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if not 'Authorization' in request.headers:
            abort(401)

        data = request.headers['Authorization']
        jwt_token = str.replace(str(data), 'Bearer ', '')
        token = None
        try:
            token = jwt.decode(jwt_token, JWT_SECRET, algorithms=['HS256']).get("token")
            answer = auth_check(token)
            if not answer.get('valid'):
                abort(401)
        except:
            abort(401)
        return f(token, *args, **kws)
    return decorated_function

# @use_guard

@app.route('/login', methods=['GET'])
@app.route('/', methods=['GET'])
def index_page():
    return send_from_directory('../client/public', 'index.html')


@app.route('/<path:path>')
def local_storage(path):
    return send_from_directory('../client/public', path)


@app.route('/api/code/<code>', methods=['GET'])
def register(code):
    if code != None:
        response = requests.get(
            'https://oauth.vk.com/access_token?client_id={0}&client_secret={1}&redirect_uri={2}&code={3}&v=5.126'.format(app_id, secure_key, website_address, code))
        if response.json().get('access_token') != None:
            token = response.json().get('access_token')
            jwt_token = jwt.encode({'token' : token},JWT_SECRET, algorithm='HS256')
            resp = make_response(redirect(url_for("index_page")))
            resp.set_cookie("token", jwt_token)
            return resp
        return 'code is not valid', 400
    return 'code is not defined', 400

@app.route('/api/authcheck', methods=['GET'])
@use_guard
def auth(token):
    return answer_template({"auth": True})

@app.route("/api/login")
def login_page():
    return redirect(
        "https://oauth.vk.com/authorize?client_id={0}&display=page&redirect_uri={1}&scope=video,stories,offline&response_type=code&v=5.126".format(
            app_id, website_address),
        code=302)
