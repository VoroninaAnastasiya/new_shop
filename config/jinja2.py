from jinja2 import Environment
from django.urls import reverse
from django.templatetags.static import static

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'url': reverse,
        'static': static,
    })
    return env

# from jinja2 import Environment
# from django.urls import reverse
#
# def environment(**options):
#     env = Environment(**options)
#     env.globals.update({
#         'url': reverse,   # чтобы можно было использовать url() как в Django
#     })
#     return env
