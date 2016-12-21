#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : ming
date   : 2016/11/27 上午12:20
role   : Version Update
'''

from tornado import web
from tornado.web import HTTPError


class IndexHandler(web.RequestHandler):
    def get(self, room):
        if room == 'get':
            raise HTTPError(500)
        self.room = room
        self.render('index.html', room=self.room, host=self.request.host)
