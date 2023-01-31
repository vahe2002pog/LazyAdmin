from email import message
from msilib.schema import Directory
from os import path
from functools import wraps
from urllib import response
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

DATA_DIR = './client/src/users'
PUBLIC_DIR = '../client/public'
ALLOWED_EXTENSIONS_IMAGE = {'png', 'jpg', 'jpeg'}
ALLOWED_EXTENSIONS_VIDEO = {'mp4', 'webm'}

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


def answer_template(data=None, error=None, meta=None, code=None):
    answer = {
        'data': data,
        'error': error,
        'meta': meta
    }
    return json.dumps(answer), code


def use_guard(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if not 'Authorization' in request.headers:
            abort(401)

        data = request.headers['Authorization']
        jwt_token = str.replace(str(data), 'Bearer ', '')
        token = None
        try:
            token = jwt.decode(jwt_token, JWT_SECRET,
                               algorithms=['HS256']).get("token")
            answer = auth_check(token)
            if not answer.get('valid'):
                abort(401)
        except:
            abort(401)
        return f(token, *args, **kws)
    return decorated_function


def get_user(token):
    if token not in user_cache:
        response = requests.get(
            "https://api.vk.com/method/users.get?access_token={}&fields=photo_100&v=5.126".format(token))
        user_cache[token] = response
        user_cache_stack.append(token)
    else:
        if user_cache_stack[-1] != token:
            user_cache_stack.remove(token)
            user_cache_stack.append(token)
    if len(user_cache_stack) > 100:
        del user_cache_stack[0]
    user = user_cache[token].json().get("response")
    return user


def get_groups(token):
    response = requests.get(
        "https://api.vk.com/method/groups.get?access_token={}&extended=1&filter=editor&v=5.126".format(token))
    groups = response.json().get("response").get("items")
    return groups


def get_extension(file_name):
    # return file_name.split('.')[-1].lower()
    return file_name.rsplit('.', 1)[1].lower()


def allowed_file(file_name, extensions):
    return '.' in file_name and \
        get_extension(file_name) in extensions


def clear_directory(path):
    for file_name in os.listdir(path):
        file = path + file_name
        if os.path.isfile(file):
            os.remove(file)


def get_user_watermark(user_id):
    path = DATA_DIR + '/user' + user_id + '/watermark'
    for file_name in os.listdir(path):
        if allowed_file(file_name, ALLOWED_EXTENSIONS_IMAGE):
            return file_name
    return None


def get_datetime_name():
    return str(datetime.datetime.now()).replace('-', "").replace(" ", "_").replace(":", "").replace(".", "")


@app.route('/login', methods=['GET'])
@app.route('/', methods=['GET'])
def index_page():
    return send_from_directory(PUBLIC_DIR, 'index.html')


@app.route('/<path:path>')
def local_storage(path):
    return send_from_directory(PUBLIC_DIR, path)


@app.route('/api/code/<code>', methods=['GET'])
def register(code):
    if code != None:
        response = requests.get(
            'https://oauth.vk.com/access_token?client_id={0}&client_secret={1}&redirect_uri={2}&code={3}&v=5.126'.format(app_id, secure_key, website_address, code))
        if response.json().get('access_token') != None:
            token = response.json().get('access_token')
            jwt_token = jwt.encode(
                {'token': token}, JWT_SECRET, algorithm='HS256')
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


@app.route("/api/user")
@use_guard
def user(token):
    return answer_template(get_user(token)[0])


@app.route("/api/groups")
@use_guard
def groups(token):
    return answer_template(get_groups(token))


@app.route("/user/watermark", methods=["POST"])
@use_guard
def load_watermark(token):
    if 'file' not in request.files:
        return answer_template(error="file not found", code=400)
    file = request.files['file']
    if file.filename == '':
        return answer_template(error="file not found", code=400)
    user_id = str(get_user(token)[0].get('id'))
    file_name = file.filename
    if file and allowed_file(file_name, ALLOWED_EXTENSIONS_IMAGE):
        file_name = "watermark." + get_extension(file_name)
        path = DATA_DIR + '/user' + user_id + "/watermark/"
        os.makedirs(path, exist_ok=True)
        clear_directory(path)
        file.save(os.path.join(path, file_name))
        return answer_template(code=200)
    else:
        return answer_template(error="wrong file extension", code=415)


@app.route("/user/watermark", methods=["GET"])
@use_guard
def get_watermark(token):
    user_id = str(get_user(token)[0].get('id'))
    watermark = get_user_watermark(user_id)
    if watermark:
        directory = '.' + DATA_DIR + '/user' + user_id + '/watermark'
        return send_from_directory(directory, watermark)
    else:
        return answer_template(error="image not found", code=404)


@app.route("/user/video", methods=["POST"])
@use_guard
def load_video(token):
    if 'file' not in request.files:
        return answer_template(error="file not found", code=400)
    video = request.files['file']
    if video.filename == '':
        return answer_template(error="file not found", code=400)
    user_id = str(get_user(token)[0].get('id'))
    video_name = video.filename
    if video and allowed_file(video_name, ALLOWED_EXTENSIONS_VIDEO):
        name = get_datetime_name()
        file_name = name + "." + get_extension(video_name)
        path = DATA_DIR + "/user" + user_id + "/videos"
        os.makedirs(path, exist_ok=True)
        file_path = os.path.join(path, file_name)
        video.save(file_path)

        my_video = Video(path, name, get_extension(video_name), video_name)

        return answer_template(code=200, data=my_video.print())
    else:
        return answer_template(error="wrong file extension", code=415)


@app.route("/user/video/preview/<preview_name>", methods=["GET"])
@use_guard
def get_video_preview(token, preview_name):
    user_id = str(get_user(token)[0].get('id'))
    directory = DATA_DIR + '/user' + user_id + '/videos/'
    file_path = directory + preview_name
    if os.path.exists(file_path):
        return send_from_directory('.' + directory, preview_name)
    else:
        return answer_template(error="image not found", code=404)

