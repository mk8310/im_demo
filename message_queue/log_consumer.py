#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : ming
date   : 2016/12/14 下午3:55
role   : Version Update
用来作为聊天记录写入的消费者
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

#
# credentials = pika.PlainCredentials(settings.MQ_USER, settings.MQ_PWD)
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(settings.MQ_ADDR, settings.MQ_PORT, settings.MQ_VHOST, credentials=credentials))

#
# def callback(ch, method, properties, body):
#     # 将消息内容写入日志，也是可以写入数据库的。。。。。。
#     logging.info(str(body))
#     ch.basic_ack(delivery_tag=method.delivery_tag)
#
#
# def create_channel():
#     channel = connection.channel()
#     channel.exchange_declare(exchange=settings.EXCHANGE, type=settings.EXCHANGE_TYPE)
#     result = channel.queue_declare(settings.LOG_QUEUE, durable=True)
#     channel.queue_bind(exchange=settings.EXCHANGE, queue=result.method.queue)
#
#     channel.basic_consume(callback,
#                           queue=result.method.queue,
#                           no_ack=False)
#     print(' [*] IM queue %s was started. Waiting for messages.' % result.method.queue)
#
#     # 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理。按ctrl+c退出。
#     channel.start_consuming()
#
#
# if __name__ == '__main__':
#     logfile_name = os.path.join(os.path.dirname(__file__), 'message.log')
#     logging.basicConfig(level=logging.INFO,
#                         format='%(asctime)s %(message)s',
#                         datefmt='%Y-%m-%d %H:%M:%S',
#                         filename=logfile_name,
#                         filemode='w')
#     logger = logging.getLogger(__name__)
#     create_channel()
