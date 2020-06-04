#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/4 0004 20:53
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : controller.py
from flask import render_template, Flask

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template('index.html')
