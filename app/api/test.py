# coding=utf-8
from flask import Flask
from flask import g
from . import api

app = Flask(__name__)


@api.route("/index")
def index():
    return "<h1 style='color:#f70'>puleya</h1>"
