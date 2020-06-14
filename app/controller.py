#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/4 0004 20:53
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : controller.py
import sanic
from jinja2 import Environment, PackageLoader
from sanic import Sanic
from sanic.exceptions import NotFound
from sanic.response import html
from sanic.websocket import WebSocketProtocol
import sys

sys.path.append("/root/dialog_system")
from app.service import data_handler

env = Environment(loader=PackageLoader('app', 'templates'))

app = Sanic(__name__)


@app.route('/')
async def index(request):
    template = env.get_template('index.html')
    html_content = template.render(title='在线陪你聊天呀')
    return html(html_content)


@app.websocket('/chat')
async def chat(request, ws):
    while True:
        msg = await ws.recv()
        print('Received: ' + msg)
        # intelligence_data = {"key": "free", "appid": 0, "msg": user_msg}
        # r = httpx.get("http://api.qingyunke.com/api.php", params=intelligence_data)
        # chat_msg = r.json()["content"]
        reply = data_handler.get_answer(msg)
        print('Sending: ' + reply)
        await ws.send(reply)


if __name__ == "__main__":
    app.error_handler.add(
        NotFound,
        lambda r, e: sanic.response.empty(status=404)
    )
    app.run(host="127.0.0.1", port=8080, protocol=WebSocketProtocol, debug=True)
