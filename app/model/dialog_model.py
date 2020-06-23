#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/23 0023 20:29
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : dialog_model.py
import re
import jieba
import numpy as np
import pandas as pd
from functools import reduce
from collections import defaultdict
from app.util.cfg_operator import config
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


def load_data():
    path = config.get_config('train_data_path')
    data = pd.read_csv(path, encoding='utf-8')
    questions = data.get('question')
    answer = data.get('answer')
    stop_words = load_stop_words()
    word_dict = defaultdict()
    for each in range(len(questions)):
        try:
            generate_index_dict(questions[each], each, stop_words, word_dict)
        except Exception:
            print(each)
            print(questions[each])
    return word_dict, stop_words, answer, questions


def handle_corpus():
    path = config.get_config('train_data_path')
    data = pd.read_csv(path, encoding='utf-8')
    questions = data.get('question')
    answer = data.get('answer')
    corpus = []
    for each in range(len(questions)):
        try:
            words = jieba.lcut(questions[each] + '，' + answer[each])
            # temp = []
            # for word in words:
            #     w = re.match('[\u4e00-\u9fa5]', word, False)
            #     if w is not None:
            #         temp.append(w.string)
            # if len(temp) <= 0:
            #     continue
            sen = reduce(lambda x, y: x + ' ' + y, words)
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
        # if each in stop_words:
        #     continue
        w = re.match('[\u4e00-\u9fa5]', each, False)
        if w is None:
            continue
        temp = word_dict.get(each)
        if temp is not None:
            temp.append(index)
            continue
        word_dict[each] = [index]
    return word_dict


def search_word(sentence, stop_words, word_dict):
    words = jieba.lcut(sentence)
    print('words:{}'.format(words))
    temp_word = []
    for each in words:
        if each in stop_words:
            continue
        temp_word.append(each)
    if len(temp_word) < 2:
        temp_word = words
    temp = []
    for each in temp_word:
        word_in_doc = word_dict.get(each)
        if word_in_doc is None:
            # print("未找到词:" + each)
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


def train_vector():
    corpus = handle_corpus()
    vector = CountVectorizer()
    X = vector.fit_transform(corpus)
    word = vector.get_feature_names()
    transformer = TfidfTransformer()
    tf_idf = transformer.fit_transform(X)
    return word, tf_idf, X, corpus


def rank_answer(indexes):
    # 获取句子的向量，第i个句子的索引，找到对应句子的向量
    max_idf = 0
    index = []
    for i in indexes:
        size = len(list(tf_idf[i].data))
        if size <= 0:
            continue
        avg_idf = np.average(tf_idf[i].data)
        if avg_idf > max_idf:
            max_idf = avg_idf
            index.clear()
        if avg_idf == max_idf:
            index.append(i)
    return index


word, tf_idf, X, corpus = train_vector()
word_dict, stop_words, answer, questions = load_data()
