from django.db import models


# Create your models here.
class Brand(models.Model):
    """ Модель бренда (Brand).

        Назначение:
        - хранит информацию о брендах, к которым относятся товары;
        - используется для фильтрации, группировки и отображения товаров по брендам;
        - отображается в каталоге, на страницах брендов и в административной панели.

        Поля:
        - name — название бренда. Уникальное, чтобы избежать дублирования.
          verbose_name и help_text помогают при работе в админке.
        - image — изображение бренда (логотип). Необязательное поле.
          Хранится в MEDIA_ROOT/img/.
        - created_at — дата создания записи.
        - updated_at — дата последнего обновления.

        Особенности:
        - unique=True гарантирует, что бренд не будет создан дважды;
        - используется в Product как ForeignKey, что позволяет связать товар с брендом;
        - может быть расширена дополнительными полями (описание, сайт, страна);
        - применяется в HTML‑вьюхах BrandsHTMLView и BrandProductsHTMLView.

        Строковое представление:
        - возвращает название бренда, что удобно для отображения в админке и логах.
        """
    name = models.CharField(max_length=150, unique=True, verbose_name='Название бренда',
                            help_text='Введите название бренда')
    image = models.ImageField(upload_to='img', blank=True, null=True, verbose_name='Картинка бренда')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        #улучшает отображение модели в Django Admin
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"