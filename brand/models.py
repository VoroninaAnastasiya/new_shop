from django.db import models


# Create your models here.
class Brand(models.Model):
    # добавить инфо о сторе, адрес, к какой компании он относится
    name = models.CharField(max_length=150, unique=True, verbose_name='Название бренда', help_text='Введите название бренда')
    image = models.ImageField(upload_to='img', blank=True, null=True, verbose_name='Картинка бренда')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name