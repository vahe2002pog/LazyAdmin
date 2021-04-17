from os import path
from flask import (abort, jsonify, make_response, redirect, render_template,
                   request, send_from_directory, url_for, Markup, Response)
import random
import math
import os
import re
import datetime

from app import app

from app.classes.video import Video
from app.config import service_token, secure_key, app_id, website_address

from pip._vendor import requests
import json

DATA_DIR = './app/users'
ALLOWED_EXTENSIONS_IMAGE = {'png', 'jpg', 'jpeg'}
ALLOWED_EXTENSIONS_VIDEO = {'mp4', 'webm'}
user_cache = dict()
user_cache_stack = []


def get_svg_by_name(file_name, stroke_color=None, fill_color=None):
    file = open("./app/src/icons/{}.svg".format(file_name))
    line = file.read().replace("\n", " ")
    file.close()
    if stroke_color != None:
        line = re.sub(r'\/\*s\*\/.+\/\*s\*\/', stroke_color, line)
    if fill_color != None:
        line = re.sub(r'\/\*f\*\/.+\/\*f\*\/', fill_color, line)
    return line

def get_extension(file_name):
    return file_name.split(".")[-1]

def get_name(file_name, extension=None):
    if extension == None:
        extension = get_extension(file_name)
    name = file_name.replace("."+extension, "")
    return name

def get_datetime_name():
    text = str(datetime.datetime.now()).replace('-', "")
    text = text.replace(" ", "_")
    text = text.replace(":", "")
    text = text.replace(".", "")
    return text

def allowed_file(file_name, extensions):
    return '.' in file_name and \
           file_name.rsplit('.', 1)[1].lower() in extensions

def auth_check(token):
    response = requests.get(
        "https://api.vk.com/method/secure.checkToken?token={0}&client_secret={1}&access_token={2}&v=5.126".format(
            token, secure_key, service_token))
    if response.json().get("response") != None:
        return {"valid": True, "user_id": response.json().get("response").get("user_id")}
    else:
        return {"valid": False}

def get_groups(token):
    response = requests.get(
        "https://api.vk.com/method/groups.get?access_token={}&extended=1&filter=editor&v=5.126".format(token))
    groups = response.json().get("response").get("items")
    return groups

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


@app.route("/", methods=["GET"])
def index_page():
    code = request.args.get("code")
    if code != None:
        response = requests.get(
            "https://oauth.vk.com/access_token?client_id={0}&client_secret={1}&redirect_uri={2}&code={3}&v=5.126".format(app_id, secure_key, website_address, code))
        if response.json().get("access_token") != None:
            token = response.json().get("access_token")
            resp = make_response(redirect(url_for("main_page")))
            resp.set_cookie("token", token)
            return resp
        else:
            return redirect(url_for("error_page", error=response.json().get("error")))
    token = request.cookies.get("token")
    if token != None:
        answer = auth_check(token)
        if answer.get("valid") == True:
            return redirect(url_for("main_page"))

    svg = Markup(get_svg_by_name("VK-logo"))

    re_authorization = request.args.get("re_authorization")

    if re_authorization != None:
        return render_template("index.html", svg=svg, re_authorization=True)

    return render_template("index.html", svg=Markup(svg), re_authorization=False)


@app.route("/login")
def login_page():
    token = request.cookies.get("token")
    if token != None:
        answer = auth_check(token)
        if answer.get("valid") == True:
            return redirect(url_for("main_page"))
    return redirect(
        "https://oauth.vk.com/authorize?client_id={0}&display=page&redirect_uri={1}&scope=video,stories,offline&response_type=code&v=5.126".format(
            app_id, website_address),
        code=302)


@app.route("/error", methods=["GET"])
def error_page():
    error = request.args.get("error")
    return render_template("error.html", error=error)


@app.route("/main")
def main_page():
    token = request.cookies.get("token")
    if token != None:
        answer = auth_check(token)
        if answer.get("valid") == True:
            groups = get_groups(token)
            user = get_user(token)[0]
            logo = ""
            for ext in ALLOWED_EXTENSIONS_IMAGE:
                path = "./app/users/user{0}/logo.{1}".format(
                    user.get("id"), ext)
                if os.path.isfile(path):
                    logo = ext
                    break
            svg_arrow_down = Markup(get_svg_by_name("ArrowDown"))
            svg_fullscreen = Markup(get_svg_by_name("FullScreen"))
            svg_drop_file = Markup(get_svg_by_name("DropFile"))
            n = math.floor(random.random() * 100)
            return render_template("main.html", groups=groups, user=user, svg_arrow_down=svg_arrow_down, svg_fullscreen=svg_fullscreen, logo=logo, n=n, svg_drop_file=svg_drop_file)
    else:
        return redirect(url_for("index_page", re_authorization=1))

    return redirect(url_for("index_page"))


@app.route("/imageLoad", methods=["POST"])
def imageLoad():
    if 'file' not in request.files:
        return "Not file"
    token = request.cookies.get("token")
    if token != None:
        answer = auth_check(token)
        if answer.get("valid") == True:
            user = get_user(token)[0]
            image_file = request.files['file']
            if image_file.filename == '':
                return "Not file"
            if image_file and allowed_file(image_file.filename, ALLOWED_EXTENSIONS_IMAGE):
                file_name = "logo." + get_extension(image_file.filename)
                path = DATA_DIR + "/user" + str(user.get("id"))
                os.makedirs(path, exist_ok=True)
                for ext in ALLOWED_EXTENSIONS_IMAGE:
                    file = path + "/logo." + ext
                    if os.path.isfile(file):
                        os.remove(file)
                image_file.save(os.path.join(path, file_name))
                return file_name
            return "Not file"
    else:
        return redirect(url_for("index_page", re_authorization=1))


@app.route("/users/<path:file_name>")
def get_files(file_name):
    token = request.cookies.get("token")
    if token != None:
        answer = auth_check(token)
        if answer.get("valid") == True:
            user = get_user(token)[0]
            path = "user" + str(user.get("id")) + "/" + file_name
            return send_from_directory("users", path)
    else:
        return redirect(url_for("index_page", re_authorization=1))


@app.route("/src/<path:path>")
def src(path):
    return send_from_directory("src", path)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory("./", "favicon.ico")


@app.route("/icons/<path:icon>", methods=["GET"])
def icon(icon):
    stroke = request.args.get("stroke")
    fill = request.args.get("fill")
    svg = get_svg_by_name(get_name(icon), stroke, fill)
    return Response(svg, mimetype="image/svg+xml")


@app.route("/videoLoad", methods=["POST"])
def videoLoad():
    if 'file' not in request.files:
        return "Not file"
    token = request.cookies.get("token")
    if token != None:
        answer = auth_check(token)
        if answer.get("valid") == True:
            user = get_user(token)[0]
            video = request.files['file']
            if video.filename == '':
                return "Not file"
            if video and allowed_file(video.filename, ALLOWED_EXTENSIONS_VIDEO):
                name = get_datetime_name()
                file_name = name + "." + get_extension(video.filename)
                path = DATA_DIR + "/user" + str(user.get("id")) + "/videos"
                os.makedirs(path, exist_ok=True)
                file_path = os.path.join(path, file_name)
                video.save(file_path)

                my_video = Video(path, name, get_extension(
                    video.filename), video.filename)

                return my_video.print()
            return "Not file"
    else:
        return redirect(url_for("index_page", re_authorization=1))


@app.route("/videoDelete/<file_name>", methods=["DELETE"])
def videoDelete(file_name):
    if(file_name != None):
        token = request.cookies.get("token")
        if token != None:
            answer = auth_check(token)
            if answer.get("valid") == True:
                user = get_user(token)[0]
                directory = DATA_DIR + "/user" + str(user.get("id")) + "/videos/"
                if file_name == "all":
                    file_list = os.listdir(directory)
                    if len(file_list) > 0:
                        for file in file_list:
                            os.remove(directory + "/" + file)
                else:
                    video_path = directory + file_name
                    preview_path = directory + get_name(file_name) + ".jpg"
                    if os.path.isfile(video_path):
                        os.remove(video_path)
                    if os.path.isfile(preview_path):
                        os.remove(preview_path)
                return "ready"
        else:
            return redirect(url_for("index_page", re_authorization=1))
    else:
        return "not valid"

@app.route("/getVideos")
def getVideos():
    token = request.cookies.get("token")
    if token != None:
        answer = auth_check(token)
        if answer.get("valid") == True:
            user = get_user(token)[0]
            directory = DATA_DIR + "/user" + str(user.get("id")) + "/videos/"
            files = []
            file_list = os.listdir(directory)
            if len(file_list) > 0:
                for file in file_list:
                    extension = get_extension(file)
                    if extension in ALLOWED_EXTENSIONS_VIDEO:
                        my_video = Video(directory, get_name(file, extension), extension)
                        files.append(my_video.print())
                return json.dumps(files)
            else:
                return "empty"
    else:
        return redirect(url_for("index_page", re_authorization=1))