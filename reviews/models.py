from django.db import models
from django.conf import settings

class Review(models.Model):
    """Модель отзыва, используемая для отображения пользовательских впечатлений
       о магазине, товаре."""
    CATEGORY_CHOICES = [
        ('product', 'О товаре'),
        ('store', 'О магазине'),
        ('delivery', 'О доставке'),
    ]

    name = models.CharField(max_length=150)
    text = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='store'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        #улучшает отображение модели в Django Admin
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"