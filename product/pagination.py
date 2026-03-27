from rest_framework.pagination import PageNumberPagination

class ProductPagination(PageNumberPagination):
    """Класс пагинации для списка товаров.
        Назначение:
        - ограничивает количество товаров, возвращаемых в одном запросе,
          20 — количество объектов на одной странице по умолчанию;
        - позволяет клиенту управлять размером страницы через параметр page_size;
        - защищает сервер от слишком больших выборок (max_page_size)."""

    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100