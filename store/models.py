from django.db import models

# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    # pic = models.ImageField()

    def __str__(self):
        return self.name
