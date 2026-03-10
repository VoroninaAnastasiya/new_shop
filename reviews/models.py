from django.db import models
from django.conf import settings

class Review(models.Model):
    name = models.CharField(max_length=150)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

