#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/4 0004 20:51
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : data_handler.py

import pandas as pd
from app.util.cfg_operator import config


def load_data():
    path = config.get_config('data_path')
    data = pd.read_csv(path, encoding='utf-8')
    head = data.head(2)
    print(head)
    return


load_data()
