from jinja2 import Environment
from django.urls import reverse

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'url': reverse,   # чтобы можно было использовать url() как в Django
    })
    return env
