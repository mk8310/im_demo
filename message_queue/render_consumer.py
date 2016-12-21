#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : ming
date   : 2016/12/20 上午9:39
role   : Version Update
用来作为聊天记录分发的消费者
'''
import json
import logging

import settings
from message_queue.base_consumer import BaseConsumer
from views.socket import SocketHandler

logger = logging.getLogger(__name__)


class RenderConsumer(BaseConsumer):
    def __init__(self, io_loop):
        super(RenderConsumer, self).__init__(io_loop,
                                             settings.EXCHANGE,
                                             settings.EXCHANGE_TYPE,
                                             settings.ROUTING_KEY,
                                             settings.DISPLAY_QUEUE)

    def on_message(self, body):
        try:
            msg_dict = json.loads(str(body))
            SocketHandler.send_to_all(msg_dict['room'], msg_dict['nickname'], msg_dict['message'])
        except Exception as ex:
            logger.error(ex)
