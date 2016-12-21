#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : ming
date   : 2016/12/20 下午2:31
role   : Version Update
'''
import os

# rabbitmq access address
MQ_ADDR = '192.168.2.128'

# rabbitmq access port
MQ_PORT = 5672

# rabbitmq vhost
MQ_VHOST = '/'

# rabbitmq access user name
MQ_USER = 'user_admin'

# rabbitmq access user password
MQ_PWD = 'passwd_admin'

# rabbitmq exchange name
EXCHANGE = 'im.ex.message'

# rabbitmq exchange type
EXCHANGE_TYPE = 'fanout'

# rabbitmq display queue name
DISPLAY_QUEUE = 'im.queue.display'

# rabbitmq log queue name
LOG_QUEUE = 'im.queue.log'

# rabbitmq routing key
ROUTING_KEY = 'example.text'

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True,
    xsrf_cookies=True,
    cookie_secret='61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=',
)
