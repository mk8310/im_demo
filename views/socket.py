#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : ming
date   : 2016/12/19 下午2:01
role   : Version Update
'''
import json

from tornado import websocket

from message_queue.publisher import publish_message


class SocketHandler(websocket.WebSocketHandler):
    clients = []

    def __init__(self, application, request, **kwargs):
        self.room = ''
        super(SocketHandler, self).__init__(application, request, **kwargs)

    def open(self, room):
        self.room = room
        SocketHandler.clients.append(self)
        publish_message(room, str(id(self)), 'im joined.')

    def on_message(self, message):
        msg_dict = json.loads(message)
        publish_message(msg_dict['room'], msg_dict['nickname'], msg_dict['message'])

    def on_close(self):
        SocketHandler.clients.remove(self)
        publish_message(self.room, str(id(self)), 'im left.')

    @staticmethod
    def send_to_all(room, nickname, message):
        for client in SocketHandler.clients:
            if room == client.room:
                client.write_message(nickname + ' said:' + message)
