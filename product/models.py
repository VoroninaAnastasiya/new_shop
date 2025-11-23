from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название товара')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена товара')
    brand = models.ForeignKey('brand.Brand', on_delete=models.CASCADE, verbose_name='Бренд')
    description = models.TextField(blank=True, null=True, verbose_name='Описание товара')
    available_quantity = models.IntegerField(default=0, verbose_name='Товар в наличии')
    categories = models.ManyToManyField('category.Category', related_name='products', verbose_name='Категории товара')
    image = models.ImageField(upload_to='img', null=True, verbose_name='Картинка товара')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} — {self.price}"
