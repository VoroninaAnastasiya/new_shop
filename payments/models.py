from django.db import models
from order.models import Order

class Payment(models.Model):
    """Модель Оплата заказа. Имеет 4 статуса платежа, три метода оплаты.
       Каждый заказ имеет ровно один платеж. Связь OneToOne с Заказом"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('canceled', 'Отменён'),
        ('failed', 'Ошибка'),
    ]

    METHOD_CHOICES = [
        ('yookassa', 'ЮKassa'),
        ('card', 'Карта'),
        ('cash', 'Наличные'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_id = models.CharField(max_length=255, blank=True, null=True)  # id платежа в ЮKassa
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='yookassa')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Оплата заказа #{self.order.id} ({self.get_status_display()})'

    class Meta:
        #улучшает отображение модели в Django Admin
        verbose_name = "Оплата заказа"
        verbose_name_plural = "Оплаты заказов"

