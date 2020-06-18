#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/4 0004 20:51
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : data_handler.py
import re
from collections import defaultdict
from functools import reduce

import pandas as pd
from app.util.cfg_operator import config
import jieba


def load_data():
    path = config.get_config('train_data_path')
    data = pd.read_csv(path, encoding='utf-8')
    questions = data.get('question')
    answer = data.get('answer')
    stop_words = load_stop_words()
    word_dict = defaultdict()
    for each in range(len(questions)):
        try:
            generate_index_dict(questions[each] + '，' + answer[each], each, stop_words, word_dict)
        except Exception:
            print(each)
            print(questions[each])
    return word_dict, stop_words, answer


def handle_corpus():
    path = config.get_config('train_data_path')
    data = pd.read_csv(path, encoding='utf-8')
    print(data.shape)
    questions = data.get('question')
    answer = data.get('answer')
    corpus = []
    for each in range(len(questions)):
        try:
            words = jieba.lcut(questions[each] + '，' + answer[each])
            temp = []
            for word in words:
                w = re.match('[\u4e00-\u9fa5]', word, False)
                if w is not None:
                    temp.append(w.string)
            if len(temp) <= 0:
                continue
            sen = reduce(lambda x, y: x + ' ' + y, temp)
            corpus.append(sen)
        except Exception:
            print(each)
            print(questions[each])
    return corpus


def load_stop_words():
    path = config.get_config('stop_word_path')
    with open(path, encoding='utf-8') as f:
        stop_words = f.readlines()
    for i in range(len(stop_words)):
        stop_words[i] = stop_words[i].strip()
    return stop_words


def generate_index_dict(doc, index, stop_words, word_dict):
    item = jieba.lcut(doc)
    for each in item:
        if each in stop_words:
            continue
        temp = word_dict.get(each)
        if temp is not None:
            temp.append(index)
            continue
        word_dict[each] = [index]
    return word_dict


def search_word(sentence, stop_words, word_dict):
    words = jieba.lcut(sentence)
    temp = []
    for each in words:
        # if each in stop_words:
        #     continue
        word_in_doc = word_dict.get(each)
        if word_in_doc is None:
            continue
        temp.append(word_in_doc)
    if len(temp) <= 0:
        print('未在文档中找到匹配的问题。')
        return
    if len(temp) == 1:
        return temp[0]
    result = []
    for i in range(len(temp) - 1):
        if i == 0:
            result = temp[i]
        result = list(set(result).intersection(set(temp[i + 1])))
    return result


def get_answer(content):
    if content is None or len(content) <= 1:
        return "你可真是言简意赅, 臣妾不懂啊！ "
    indexes = search_word(content, stop_words, word_dict)
    if indexes is None or len(indexes) <= 0:
        return "你可说的超出我的理解范围了, 请想想再说吧！"

    return answer[indexes[0]]


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


def rank_answer(sentences):
    corpus = handle_corpus()
    print(len(corpus))
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)
    word = vectorizer.get_feature_names()
    # 类调用
    print(len(word))
    print(len(word[0]))
    print(word[0])
    print(word[1])
    transformer = TfidfTransformer()
    print(transformer)
    tf_idf = transformer.fit_transform(X)
    print(tf_idf[1])
    print(tf_idf[1].data[0])
    print(tf_idf[1].indices[0])
    for i in range(0, 5):
        print(word[tf_idf[1].indices[i]])

    return


rank_answer('')

word_dict, stop_words, answer = load_data()
