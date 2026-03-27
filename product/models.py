from django.db import models

class Product(models.Model):
    """
        Модель товара в каталоге интернет‑магазина.

        Назначение:
        - хранит основную информацию о товаре (название, цена, описание);
        - связывает товар с брендом и категориями;
        - хранит количество доступного товара на складе;
        - поддерживает загрузку изображения товара;
        - используется в каталоге, карточке товара, фильтрации и API.

        Поля:
        - name — название товара. Отображается в каталоге и карточке товара.
        - price — цена товара. DecimalField выбран для точных денежных значений,
          чтобы избежать ошибок округления, характерных для float.
        - brand — связь с моделью Brand. При удалении бренда товары удаляются
          (CASCADE), что логично для каталога.
        - description — текстовое описание. Необязательное поле.
        - available_quantity — количество товара на складе. PositiveIntegerField
          гарантирует, что значение не может быть отрицательным.
        - categories — связь ManyToMany с Category. Один товар может относиться
          к нескольким категориям, и одна категория может содержать множество товаров.
          related_name='products' позволяет обращаться к товарам через category.products.
        - image — изображение товара. Хранится в MEDIA_ROOT/img/. Поле необязательное.
        - created_at — дата создания записи. Устанавливается автоматически.
        - updated_at — дата последнего обновления. Обновляется при каждом сохранении.

        Особенности:
        - модель оптимизирована для каталога: поддерживает фильтрацию по бренду,
          категориям, цене и наличию;
        - используется в API‑эндпоинтах, HTML‑страницах и административной панели;
        - может быть расширена полями скидок, вариаций, SEO‑метаданными.

        Строковое представление:
        - возвращает название и цену товара, что удобно для отображения в админке
          и консоли.
        """

    name = models.CharField(max_length=150, verbose_name='Название товара')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена товара')
    brand = models.ForeignKey('brand.Brand', on_delete=models.CASCADE, verbose_name='Бренд')
    description = models.TextField(blank=True, null=True, verbose_name='Описание товара')
    available_quantity = models.PositiveIntegerField(default=0, verbose_name='Товар в наличии')
    categories = models.ManyToManyField('category.Category', related_name='products', verbose_name='Категории товара')
    image = models.ImageField(upload_to='img', null=True, blank=True, verbose_name='Картинка товара')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} — {self.price}"