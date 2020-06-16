#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/17 0017 0:02
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : dataset_handler.py
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

split_dataset()
