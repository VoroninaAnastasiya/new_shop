from django.db import models
from django.conf import settings
from product.models import Product
from django.db import models

class CartItem(models.Model):
    """ Модель позиции корзины (CartItem).

        Назначение:
        - представляет одну строку корзины: конкретный товар и его количество;
        - связывает пользователя и товар, позволяя каждому пользователю иметь
          собственную корзину;
        - используется при оформлении заказа, подсчёте итоговой суммы и проверке остатков.

        Поля:
        - user — пользователь, которому принадлежит корзина.
          related_name='cart_items' позволяет обращаться к корзине через:
              user.cart_items.all()
        - product — товар, добавленный в корзину. Один и тот же товар может быть
          в корзине у разных пользователей.
        - quantity — количество товара. PositiveIntegerField гарантирует, что
          значение всегда положительное.
        - added_at — дата и время добавления товара в корзину."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items')
    #позволяет обращаться к корзине через user.cart_items.all()
    product = models.ForeignKey(Product, on_delete=models.CASCADE) #Один товар может быть в корзине у многих пользователей.
    quantity = models.PositiveIntegerField(default=1) #Количество товара = только положительные числа.
    added_at = models.DateTimeField(auto_now_add=True) #Дата добавления позиции в корзину.

    class Meta:
        unique_together = ('user', 'product')#один и тот же товар
        #TODO не может быть добавлен дважды одним пользователем — только увеличивается quantity, можно доработать
        # заменив unique_together на UniqueConstraint - более современный вариант
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'

    def __str__(self):
        '''отображение в админке'''
        return f'{self.user} - {self.product.name} * {self.quantity}'

    def get_total_price(self):
        '''Метод для подсчёта общей стоимости конкретной позиции в корзине'''
        return self.product.price * self.quantity