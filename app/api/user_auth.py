# coding=utf8
from flask import Flask, request, Response
from flask import g
from . import api

from app.config import *
from app.utils.aes_utils import encrypt_aes
from .function_implements import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import timedelta
import json
import time

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024


@api.before_app_request
def init_session():
    g.engine = create_engine(DATABASE)
    g.session = sessionmaker(bind=g.engine)()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'session'):
        g.session.close()


@api.route("/addrecord")
def add_record():
    param_dict = request.args.to_dict()
    try:
        print(1)
        insert_records(g.session, param_dict)
        return encrypt_aes(json.dumps({"code": "1"}))
    except:
        return encrypt_aes(json.dumps({"code": "0"}))

@api.route("/getrecords")
def get_record():
    all_records = get_records(g.session)
    record_lis = []
    for record in all_records:
        record_lis.append(json.dumps({
            "itemname": get_itemname_by_id(g.session, record.item_id),
            "username": get_username_by_id(g.session, record.user_id),
            "last_use_time": record.last_use_time,
            "state": record.state
        }))
    return encrypt_aes(str(record_lis))


@api.route("/additem")
def add_item():
    param_dict = request.args.to_dict()
    try:
        insert_item(g.session, param_dict)
        return encrypt_aes(json.dumps({"code": "1"}))
    except:
        return encrypt_aes(json.dumps({"code": "0"}))


@api.route("/getitems")
def get_item():
    all_items = get_items(g.session)
    item_lis = []
    for item in all_items:
        item_lis.append(json.dumps({
            "itemname": item.itemname,
            "description": item.description,
            "amount": item.amount,
            "username": get_username_by_id(g.session, item._user_id)
        }))
    return encrypt_aes(str(item_lis))


@api.route("/ping")
def ping():
    return "200"


@api.route("/getuser")
def getuser():
    param_dict = request.args.to_dict()
    user = get_user(g.session, param_dict["username"])
    # username phone image_src email sign rights
    return encrypt_aes(json.dumps({
        "username": user.username,
        "phone": user.phone,
        "image_src": user.image_src,
        "email": user.email,
        "sign": user.sign,
        "rights": user.rights,
    }))


@api.route("/update")
def update():
    param_dict = request.args.to_dict()
    try:
        update_user(g.session, param_dict)
    except:
        return encrypt_aes(json.dumps({"code": "0"}))
    return encrypt_aes(json.dumps({"code": "1"}))


@api.route("/exists")
def exists():
    param_dict = request.args.to_dict()
    if "username" in param_dict.keys() and not "passwordsalt" in param_dict.keys():
        if exists_user(g.session, param_dict["username"]):
            return encrypt_aes(json.dumps({"code": "1"}))

    return encrypt_aes(json.dumps({"code": "0"}))


@api.route("/login")
def login():
    param_dict = request.args.to_dict()
    if "username" in param_dict.keys() and "passwordsalt" in param_dict.keys():
        if exists_user(g.session, param_dict["username"], param_dict["passwordsalt"]):
            return encrypt_aes(json.dumps({"code": "1"}))
    return encrypt_aes(json.dumps({"code": "0"}))


@api.route("/insert")
def insert():
    param_dict = request.args.to_dict()
    try:
        insert_user(g.session, param_dict)
        return encrypt_aes(json.dumps({"code": "1"}))
    except Exception:
        return encrypt_aes(json.dumps({"code": "0"}))


@api.route("/upload", methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files["file"]
        filename = str(time.time()) + f.filename
        try:
            update_user_image(g.session, request.args.to_dict()["username"], filename)
            f.save(UPLOAD + filename)
            return encrypt_aes(json.dumps({"code": "1"}))
        except Exception:
            return encrypt_aes(json.dumps({"code": "0"}))
    else:
        return encrypt_aes(json.dumps({"code": "0"}))


@api.route("/getimage")
def getimage():
    image = open(UPLOAD + request.args.to_dict()["image"], "rb").read()
    resp = Response(image, mimetype="image/*")
    return resp
