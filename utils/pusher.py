import json
import logging

from django.conf import settings
from kombu import Connection, Exchange, Queue
from .renderers import CustomJSONEncoder


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs): #только один экземпляр RabbitMQPusher, только одно соединение с RabbitMQ
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


def dump_data(payload):
    return json.dumps(payload, cls=CustomJSONEncoder) #кастомный JSON‑энкодер
#
#
# @singleton
# class RabbitMQPusher: #создаётся логгер, соединение, producer единожды
#     def __init__(self):
#         self.log = logging.getLogger('RabbitmqPusher')
#         self.connection = None
#         self.producer = None
#         self.connect()
#
#     def connect(self):
#         try:
#             self.connection = Connection(
#                 hostname=settings.RABBITMQ['RABBIT_HOST'],
#                 port=settings.RABBITMQ['RABBIT_PORT'],
#                 userid=settings.RABBITMQ['RABBIT_USER'],
#                 password=settings.RABBITMQ['RABBIT_PASSWORD'],
#                 virtual_host='/',
#                 heartbeat=10,
#             )
#             self.producer = self.connection.Producer()
#             print('Core rabbitmq connected')
#             self.log.info('Core rabbitmq connected')
#         except Exception as e:
#             print(f'Core rabbitmq connect error: {e}')
#             self.log.error(f'Core rabbitmq connect error: {e}', exc_info=True)
#             raise
#
#     def error_callback(self, exc, interval):
#         self.log.error('Error: %r', exc, exc_info=1)
#         self.log.info('Retry in %s seconds.', interval)
#
#     def send(self, message, exchange, routing_key, queue=None, priority=0):
#         try:
#             self.connection.ensure_connection(
#                 errback=self.error_callback,
#                 max_retries=2,
#                 timeout=1,
#             )
#
#             exchange_obj = Exchange(exchange, type='direct')
#             queue_obj = Queue(queue, exchange_obj, routing_key=routing_key)
#
#             self.producer.publish(
#                 body=message,
#                 exchange=exchange_obj,
#                 routing_key=routing_key,
#                 declare=[exchange_obj, queue_obj],
#                 retry=True,
#                 priority=priority,
#             )
#             print("message sended")
#
#         except Exception as e:
#             print(f'Failed to deliver: {message} to {exchange} {routing_key}, e={e}')
#             self.log.exception(f'Failed to deliver: {message} to {exchange} {routing_key}')

@singleton
class RabbitMQPusher:
    def __init__(self):
        self.log = logging.getLogger('RabbitmqPusher')
        self.connection = None
        self.producer = None
        self.connect()

    def connect(self):
        try:
            # создаём объект соединения
            self.connection = Connection(
                hostname=settings.RABBITMQ['RABBIT_HOST'],
                port=settings.RABBITMQ['RABBIT_PORT'],
                userid=settings.RABBITMQ['RABBIT_USER'],
                password=settings.RABBITMQ['RABBIT_PASSWORD'],
                virtual_host='/',
                heartbeat=10,
            )

            # ОТКРЫВАЕМ соединение сразу
            self.connection.connect()

            # создаём producer поверх открытого соединения
            self.producer = self.connection.Producer()

            print('RabbitMQ persistent connection established')
            self.log.info('RabbitMQ persistent connection established')

        except Exception as e:
            print(f'RabbitMQ connect error: {e}')
            self.log.error(f'RabbitMQ connect error: {e}', exc_info=True)
            raise

    def error_callback(self, exc, interval):
        self.log.error('Error: %r', exc, exc_info=1)
        self.log.info('Retry in %s seconds.', interval)

    def send(self, message, exchange, routing_key, queue=None, priority=0):
        try:
            # если соединение разорвано — переподключаемся
            if not self.connection.connected:
                self.connect()

            exchange_obj = Exchange(exchange, type='direct')
            queue_obj = Queue(queue, exchange_obj, routing_key=routing_key)

            self.producer.publish(
                body=message,
                exchange=exchange_obj,
                routing_key=routing_key,
                declare=[exchange_obj, queue_obj],
                retry=True,
                priority=priority,
            )

            print("message sent")

        except Exception as e:
            print(f'Failed to deliver: {message} to {exchange} {routing_key}, e={e}')
            self.log.exception(f'Failed to deliver: {message} to {exchange} {routing_key}')

