from django.db import models
from django.conf import settings
from product.models import Product
from django.db import models

class CartItem(models.Model):
    #Создаём модель CartItem, которая представляет одну позицию в корзине (один товар с количеством)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items')
    #позволяет обращаться к корзине через user.cart_items.all()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')#один и тот же товар
        #TODO не может быть добавлен дважды одним пользователем — только увеличивается quantity, можно доработать
        # заменив unique_together на UniqueConstraint - более современный вариант
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'

    def __str__(self):
        return f'{self.user} - {self.product.name} * {self.quantity}'

    def get_total_price(self):
        #Метод для подсчёта общей стоимости конкретной позиции в корзине.
        return self.product.price * self.quantity
