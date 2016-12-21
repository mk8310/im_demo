#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : ming
date   : 2016/12/14 下午3:55
role   : Version Update
模拟聊天记录持久化消费者
'''

import logging

import settings
from message_queue.base_consumer import BaseConsumer

logger = logging.getLogger(__name__)


class LogConsumer(BaseConsumer):
    """
    模拟聊天记录持久化
    """
    def __init__(self, io_loop):
        super(LogConsumer, self).__init__(io_loop,
                                          settings.EXCHANGE,
                                          settings.EXCHANGE_TYPE,
                                          settings.ROUTING_KEY,
                                          settings.LOG_QUEUE)

    def on_message(self, body):
        try:
            logging.info(str(body))
        except Exception as ex:
            logger.error(ex)
