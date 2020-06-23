#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/4 0004 20:51
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : data_handler.py


import httpx
import app.model.dialog_model as model


def get_answer(content):
    if content is None or len(content) <= 1:
        return "你可真是言简意赅, 臣妾不懂啊！ "
    indexes = model.search_word(content, model.stop_words, model.word_dict)
    print('searched indexes:\n{}'.format(indexes))
    if indexes is None or len(indexes) <= 0:
        intelligence_data = {"key": "free", "appid": 0, "msg": content}
        r = httpx.get("http://api.qingyunke.com/api.php", params=intelligence_data)
        response = r.json()["content"]
        return response
    ranked = model.rank_answer(indexes)
    for i in ranked:
        print(model.questions[i] + ':' + model.answer[i])
    return model.answer[ranked[0]]
