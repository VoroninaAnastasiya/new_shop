from django.http import HttpResponse
from .sender import send_to_queue


def test_rabbit(request):
    send_to_queue(
        exchange='test_exchange',
        routing_key='test.key',
        queue='test_queue',
        payload={
            'url': f'http://localhost:8000/test-rabbit/reciver/',
            'method': 'POST',
            'message': 'Hello from Django!'
        },
    )
    return HttpResponse("Message sent to RabbitMQ")


def test_rabbit_reciver(request):
    print(f"take message {request.dict()}")
