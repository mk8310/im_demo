#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : ming
date   : 2016/12/20 下午1:53
role   : Version Update
聊天记录分发的生产者
'''
import json

import pika

import settings


def publish_message(method, nickname, message):
    credentials = pika.PlainCredentials(settings.MQ_USER, settings.MQ_PWD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(settings.MQ_ADDR, settings.MQ_PORT, settings.MQ_VHOST, credentials=credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange=settings.EXCHANGE, type=settings.EXCHANGE_TYPE)

    dict_content = {'room': method, 'nickname': nickname, 'message': message}
    content = json.dumps(dict_content)

    properties = pika.BasicProperties(content_type='application/json')

    channel.basic_publish(exchange=settings.EXCHANGE,
                          routing_key='',
                          body=content,
                          properties=properties)
