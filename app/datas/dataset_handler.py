#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/17 0017 0:02
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : dataset_handler.py
import re

import jieba

from app.util.cfg_operator import config
import pandas as pd


def split_dataset():
    path = config.get_config('data_path')
    data = pd.read_csv(path, encoding='utf-8')
    shuffle_data = data.sample(frac=1.0).reset_index()
    train_num = int(shuffle_data.shape[0] * 0.8)
    train_data = shuffle_data.loc[0:train_num].drop(labels='index', axis=1)
    test_data = shuffle_data.loc[train_num + 1:].drop(labels='index', axis=1)
    train_data.to_csv("../datas/train_data.csv", index=False)
    test_data.to_csv("../datas/test_data.csv", index=False)
    return


def clean_data(input_path, out_path):
    data = pd.read_csv(input_path, encoding='utf-8')
    print(data.shape)
    questions = data.get('question')
    answer = data.get('answer')
    q = []
    a = []
    for each in range(len(questions)):
        try:
            words = jieba.lcut(questions[each] + '，' + answer[each])
            for word in words:
                w = re.match('[\u4e00-\u9fa5]', word, False)
                if w is None:
                    print(questions[each])
                    continue
                q.append(questions[each])
                a.append(answer[each])
                break
        except Exception:
            print(questions[each])
    name = ['question', 'answer']
    data_set = [q, a]
    print(len(q))
    print(len(a))
    cleaned_data = pd.DataFrame(columns=name, data=data_set)  # 数据有三列，列名分别为one,two,three
    cleaned_data.to_csv(out_path, encoding='utf-8')
    return


# split_dataset()
clean_data('../datas/train_data.csv', '../datas/cleaned_train_data.csv')
