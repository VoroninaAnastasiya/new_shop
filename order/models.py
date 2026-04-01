from django.db import models
from django.conf import settings
from product.models import Product


class Order(models.Model):
    """Модель заказа. Каждый экземпляр представляет собой один оформленный заказ пользователя.

    Назначение:
    - хранит информацию о пользователе, статусе, способе оплаты и доставки;
    - содержит адрес, дату и время доставки, комментарий;
    - хранит итоговую сумму заказа (total_price);
    - связывается с позициями заказа через related_name='items';
    - используется в оформлении заказа, оплате, email‑уведомлениях и админке.

    Методы:
    - calculate_total():
        Пересчитывает сумму заказа как сумму total_price всех связанных OrderItem.
        Используется во viewset после создания позиций заказа.
    - save():
        Переопределён для исключения автоматического пересчёта total_price.
        Логика пересчёта вынесена во viewset, чтобы избежать двойных сохранений.
    """
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending') #По умолчанию — ожидает оплаты.
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
        '''Пересчитывает сумму заказа как сумму total_price'''
        self.total_price = sum(item.total_price for item in self.items.all())
        return self.total_price

    def save(self, *args, **kwargs):
        '''пересчёт суммы вынесен в viewset.'''
        super().save(*args, **kwargs)
        # правка от 16.02, было - super().save(update_fields=['total_price'])

    def __str__(self):
        return f"Order {self.id} by {self.user}"

    class Meta:
        #улучшает отображение модели в Django Admin
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    """Позиция заказа — отдельный товар в составе заказа.

        Назначение:
        - хранит ссылку на товар и его количество;
        - хранит total_price для конкретной позиции (price * quantity);
        - используется для формирования итоговой суммы заказа.

        Поля:
        - order — ссылка на заказ. При удалении заказа удаляются все его позиции.
        - product — товар, который был добавлен в заказ.
        - quantity — количество товара.
        - total_price — итоговая стоимость позиции (product.price * quantity).

        Методы:
        - calculate_total():
            Рассчитывает total_price позиции.
            Если у товара нет цены — выбрасывает исключение.

        - save():
            Переопределён, но логика пересчёта вынесена во viewset.
            Это позволяет избежать лишних сохранений и циклических вызовов.

        Особенности:
        - related_name='items' позволяет обращаться к позициям через order.items.all();
        - total_price хранится в базе для ускорения выборок и формирования email‑уведомлений;
        - логика пересчёта вынесена в бизнес‑слой (viewset), что делает систему гибче.
        """
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
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"