#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/23 0023 20:29
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : validation.py
import pandas as pd

import app.model.dialog_model as model
from app.util.cfg_operator import config


def load_test_data():
    path = config.get_config('test_data_path')
    data = pd.read_csv(path, encoding='utf-8')
    sample = data.sample(10).reset_index()
    # print(sample)
    questions = sample.get('question')
    answer = sample.get('answer')
    return questions, answer


def validate():
    ques, ans = load_test_data()
    count = 0
    for each in range(len(ques)):
        indexes = model.search_word(ques[each], model.stop_words, model.word_dict)
        if indexes is None or len(indexes) == 0:
            print("未找到符合的结果-->{}".format(ques[each]))
            count += 1
            continue
        ranked = model.rank_answer(indexes)
        # for i in ranked:
        #     print(model.questions[i] + ':' + model.answer[i])
        result = model.answer[ranked[0]]
        print("生成的结果为：{}".format(result))
        print("实际结果为：{}".format(ans[each]))
    print('precision:{}'.format((1 - count / 10.0)))
    return


validate()
