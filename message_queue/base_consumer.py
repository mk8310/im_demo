#!/usr/bin/env python
# -*-coding:utf-8-*-
'''
Author : ming
date   : 2016/12/21 下午1:20
role   : Version Update
'''
import logging
from abc import ABCMeta, abstractmethod

import pika
from pika import TornadoConnection

from settings import MQ_USER, MQ_PWD, MQ_ADDR, MQ_PORT, MQ_VHOST

logger = logging.getLogger(__name__)


class BaseConsumer(object):
    __metaclass__ = ABCMeta

    """
        Pika-Tornado connection setup
        The setup process is a series of callback methods.
        connect:connect to rabbitmq and build connection to tornado io loop ->
        on_connected: create a channel to rabbitmq ->
        on_channel_open: declare queue tornado, bind that queue to exchange
                         chatserver_out and start consuming messages.
       """

    def __init__(self, io_loop, exchange_name, exchange_type, routing_key, queue_name):
        logger.info('%s: __init__' % self.__class__.__name__)
        self._io_loop = io_loop

        self._connected = False
        self._connecting = False
        self._connection = None
        self._channel = None
        self._message_count = 0
        self._exchange_name = exchange_name
        self._exchange_type = exchange_type
        self.routing_key = routing_key
        self._queue_name = queue_name

    def on_channel_open(self, channel):
        logger.info('%s: Channel %s open, Declaring exchange' % (self.__class__.__name__, channel))
        self._channel = channel
        logger.info('Declaring exchange %s', self._exchange_name)
        self._channel.exchange_declare(self.on_exchange_declareok,
                                       self._exchange_name,
                                       self._exchange_type)

    def on_connected(self, connection):
        logger.info('%s: connected to RabbitMQ' % self.__class__.__name__)
        self._connected = True
        self._connection = connection
        # now you are able to call the pika api to do things
        # this could be exchange setup for websocket connections to
        # basic_publish to later.
        self._connection.channel(self.on_channel_open)

    def on_closed(self, connection):
        logger.info('%s: rabbit connection closed' % self.__class__.__name__)
        self._io_loop.stop()

    def connect(self):
        if self._connecting:
            logger.info('%s: Already connecting to RabbitMQ' % self.__class__.__name__)
            return

        logger.info('%s: Connecting to RabbitMQ' % self.__class__.__name__)
        self._connecting = True

        cred = pika.PlainCredentials(MQ_USER, MQ_PWD)
        param = pika.ConnectionParameters(
            host=MQ_ADDR,
            port=MQ_PORT,
            virtual_host=MQ_VHOST,
            credentials=cred
        )
        self._connection = TornadoConnection(param, on_open_callback=self.on_connected, stop_ioloop_on_close=False)
        self._connection.add_on_close_callback(self.on_closed)

    def on_exchange_declareok(self, unused_frame):
        """Invoked by pika when RabbitMQ has finished the Exchange.Declare RPC
        command.

        :param pika.Frame.Method unused_frame: Exchange.DeclareOk response frame

        """
        logger.info('Exchange declared')
        logger.info('Declaring queue %s', self._queue_name)
        self._channel.queue_declare(self.on_queue_declareok, self._queue_name, durable=True)

    def message_callback(self, unused_channel, basic_deliver, properties, body):
        """Invoked by pika when a message is delivered from RabbitMQ. The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.

        :param pika.channel.Channel unused_channel: The channel object
        :param pika.Spec.Basic.Deliver: basic_deliver method
        :param pika.Spec.BasicProperties: properties
        :param str|unicode body: The message body

        """
        logger.info('Received message # %s from %s: %s',
                    basic_deliver.delivery_tag, properties.app_id, body)
        self.on_message(body)
        self.acknowledge_message(basic_deliver.delivery_tag)

    @abstractmethod
    def on_message(self, body):
        """The event on the message recieved.
        :param body: The message body.

        """
        pass

    def start_consuming(self):
        """This method sets up the consumer by first calling
        add_on_cancel_callback so that the object is notified if RabbitMQ
        cancels the consumer. It then issues the Basic.Consume RPC command
        which returns the consumer tag that is used to uniquely identify the
        consumer with RabbitMQ. We keep the value to use it when we want to
        cancel consuming. The message_callback method is passed in as a callback pika
        will invoke when a message is fully received.

        """
        logger.info('Issuing consumer related RPC commands')
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(self.message_callback, self._queue_name)

    def on_bindok(self, unused_frame):
        """Invoked by pika when the Queue.Bind method has completed. At this
        point we will start consuming messages by calling start_consuming
        which will invoke the needed RPC commands to start the process.

        :param pika.frame.Method unused_frame: The Queue.BindOk response frame

        """
        logger.info('Queue bound')
        self.start_consuming()

    def on_queue_declareok(self, method_frame):
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. In this method we will bind the queue
        and exchange together with the routing key by issuing the Queue.Bind
        RPC command. When this command is complete, the on_bindok method will
        be invoked by pika.

        :param pika.frame.Method method_frame: The Queue.DeclareOk frame

        """
        logger.info('Binding %s to %s', self._exchange_name, self._queue_name)
        self._channel.queue_bind(self.on_bindok, self._queue_name, self._exchange_name)

    def acknowledge_message(self, delivery_tag):
        """Acknowledge the message delivery from RabbitMQ by sending a
        Basic.Ack RPC method for the delivery tag.

        :param int delivery_tag: The delivery tag from the Basic.Deliver frame

        """
        logger.info('Acknowledging message %s', delivery_tag)
        self._channel.basic_ack(delivery_tag)

    def on_consumer_cancelled(self, method_frame):
        """Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer
        receiving messages.

        :param pika.frame.Method method_frame: The Basic.Cancel frame

        """
        logger.info('Consumer was cancelled remotely, shutting down: %r',
                    method_frame)
        if self._channel:
            self._channel.close()

    def add_on_cancel_callback(self):
        """Add a callback that will be invoked if RabbitMQ cancels the consumer
        for some reason. If RabbitMQ does cancel the consumer,
        on_consumer_cancelled will be invoked by pika.

        """
        logger.info('Adding consumer cancellation callback')
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)
