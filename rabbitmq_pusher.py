import json
import logging

from django.conf import settings

from common.queue import Connection
from common.renderers import CustomJSONEncoder


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


def dump_data(payload):
    return json.dumps(payload, cls=CustomJSONEncoder)


@singleton
class RabbitMQPusher:
    def __init__(self):
        self.log = logging.getLogger('RabbitmqPusher')
        self.connection = None
        self.producer = None
        self.connect()

    def connect(self):
        try:
            self.connection = Connection(
                hostname=settings.RABBITMQ['RABBIT_HOST'],
                port=settings.RABBITMQ['RABBIT_PORT'],
                userid=settings.RABBITMQ['RABBIT_USER'],
                password=settings.RABBITMQ['RABBIT_PASSWORD'],
                virtual_host='/',
                heartbeat=10,
            )
            self.producer = self.connection.Producer()
            self.log.info('Core rabbitmq connected')
        except Exception as e:
            self.log.error(f'Core rabbitmq connect error: {e}', exc_info=True)
            raise

    def error_callback(self, exc, interval):
        self.log.error('Error: %r', exc, exc_info=1)
        self.log.info('Retry in %s seconds.', interval)

    def send(self, message, exchange, routing_key, queue=None, priority=0):
        if settings.DISABLE_RABBITMQ:
            assert json.dumps(message)
            return

        try:
            self.connection.ensure_connection(
                errback=self.error_callback,
                max_retries=2,
                timeout=1,
            )
            self.producer.publish(
                body=message,
                exchange=exchange,
                routing_key=routing_key,
                declare=[exchange, queue],
                retry=True,
                priority=priority,
            )
        except Exception:
            self.log.exception(f'Failed to deliver: {message} to {exchange} {routing_key}')

# kombu moves msg from unacked to ready after timeout
