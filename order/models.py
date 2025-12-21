from django.db import models
from django.conf import settings
from product.models import Product

# Create your models here.
class Order(models.Model):
    '''Определяет таблицу заказов. Каждый экземпляр — отдельный заказ.'''
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('paid', 'Оплачен'),
        ('shipped', 'Отправлен'),
        ('completed', 'Завершён'),
        ('canceled', 'Отменён'),
    ]

    PAYMENT_CHOICES = [
        ('card', 'Банковская карта'),
        ('cash', 'Наличные'),
        ('online', 'Оплата онлайн')
    ]

    DELIVERY_CHOICES = [
        ('pickup', 'Самовывоз'),
        ('courier', 'Курьерская доставка')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    #добавляет обратный доступ: у user появится user.orders.all()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    city = models.CharField(max_length=80)
    address = models.CharField(max_length=255, blank=True, null=True)
    payment_type = models.CharField(max_length=25, choices=PAYMENT_CHOICES, default='card')
    delivery_type = models.CharField(max_length=25, choices=DELIVERY_CHOICES, default='pickup')
    delivery_data = models.DateField(blank=True, null=True)
    delivery_time = models.TimeField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} by {self.user}"


class OrderItem(models.Model):
    '''Определяет строку заказа (позицию) — конкретный продукт и его количество в составе заказа.'''
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"