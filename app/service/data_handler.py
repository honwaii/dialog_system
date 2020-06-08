#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/4 0004 20:51
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : data_handler.py

import pandas as pd
from app.util.cfg_operator import config
import jieba


def load_data():
    path = config.get_config('data_path')
    data = pd.read_csv(path, encoding='utf-8')
    questions = data.get('question')
    stop_words = load_stop_words()
    results = []
    for each in range(len(questions)):
        try:
            q = jieba.lcut(questions[each])
            result = []
            for e in q:
                if e in stop_words:
                    continue
                result.append(e)
            results.append(result)
        except Exception:
            print(each)
    print(results[0])
    print(results[1])
    return


def load_stop_words():
    path = config.get_config('stop_word_path')
    with open(path, encoding='utf-8') as f:
        stop_words = f.readlines()
        # print(len(stop_words))
    return stop_words


load_data()
# load_stop_words()
