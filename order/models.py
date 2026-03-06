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
        ('crypto', 'Крипта') #! TODO решить, надо ли реализовывать такую фичу? как?
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
    is_registered = models.BooleanField(default=False)#TODO для чего делала это поле??? “заказ оформлен”?
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_total(self):
        self.total_price = sum(item.total_price for item in self.items.all())
        return self.total_price

    def save(self, *args, **kwargs):
        # self.calculate_total()
        super().save(*args, **kwargs)
        # правка от 16.02, было - super().save(update_fields=['total_price'])

    def __str__(self):
        return f"Order {self.id} by {self.user}"


class OrderItem(models.Model):
    '''Определяет строку заказа (позицию) — конкретный продукт и его количество в составе заказа.'''
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_total(self):
        if self.product.price is not None:
            self.total_price = self.product.price * self.quantity
        else:
            raise ValueError(f"Цена товара '{self.product.price}' не установлена")
        return self.total_price

    def save(self, *args,**kwargs):  # при сохранении пересчитываем
        # self.calculate_total() #вызов calculate_total всегда будет происходить, когда создаешь
        # или обновляешь экземпляр OrderItem
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"