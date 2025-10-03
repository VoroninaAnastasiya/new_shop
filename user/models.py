from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя пользователя')
    lastname = models.CharField(max_length=50, verbose_name='Фамилия пользователя')
    contact_phone = models.IntegerField(verbose_name='Номер телефона')
    email = models.EmailField(null=False, unique=True, verbose_name='Электронная почта')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProfileUser(models.Model):
    user_profile = models.OneToOneField(on_delete=models.CASCADE, verbose_name='Профиль пользоваеля')
    image = models.ImageField(upload_to='img', null=True, verbose_name='Аватарка пользователя')

    def __str__(self):
        return self.user_profile