#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : ming
date   : 2016/11/27 上午12:19
role   : Version Update
'''

from views.index import IndexHandler

from views.socket import SocketHandler

url_patterns = (
    (r"/soc/(?P<room>[0-9a-zA-Z\-_]+)", SocketHandler),
    (r"/im/(?P<room>[0-9a-zA-Z\-_]+)", IndexHandler),
)
