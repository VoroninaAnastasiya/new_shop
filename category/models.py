from django.db import models


# Create your models here.
class Category(models.Model):
    """ Модель категории товара.

        Назначение:
        - группирует товары по тематике или типу;
        - используется в каталоге, фильтрации, навигации и HTML‑страницах;
        - обеспечивает ManyToMany связь с Product через поле categories в модели Product.

        Поля:
        - name — название категории. Уникальное, чтобы избежать дублирования.
        - created_at — дата создания категории.
        - updated_at — дата последнего обновления.

        Особенности:
        - unique=True гарантирует, что не будет двух категорий с одинаковым названием;
        - используется в HTML‑вьюхах CategoriesHTMLView и CategoryProductsHTMLView;
        - через related_name='products' можно получить все товары категории:
            category.products.all()
        """
    name = models.CharField(max_length=150, unique=True, verbose_name='Название категории товара') #unique=True - чтобы не было двух одинаковых категорий
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        #улучшает отображение модели в Django Admin
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории"