#!/usr/bin/env python
# coding:utf-8
__author__ = 'stone'
__date__ = '2018/3/22'

import urllib


"""
读取文件URL进行解码并写入文件
"""
with open('sql.txt', 'r') as f:
    for url in f.readlines():
        url_quote = urllib.unquote(url)
        with open('unquote_url.txt', 'a') as uf:
            uf.write("{0}\n".format(url_quote))
