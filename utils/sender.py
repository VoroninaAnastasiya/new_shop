from .pusher import RabbitMQPusher, dump_data


def send_to_queue(exchange, routing_key, payload, queue=None, priority=1):
    message = dump_data(payload)
    pusher = RabbitMQPusher()
    pusher.send(
        message=message,
        exchange=exchange,
        routing_key=routing_key,
        queue=queue,
        priority=priority,
    )
