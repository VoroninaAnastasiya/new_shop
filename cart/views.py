from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CartItem
from .serializers import CartItemSerializer

class CartHTMLDetailView(APIView):
    """Представление для отображения корзины заказа конкретного пользователя в HTML."""
    renderer_classes = [TemplateHTMLRenderer]
    #permission_classes = [IsAuthenticated]
    template_name = 'cart.html'

    def get(self, request):
        if not request.user.is_authenticated: #для тестирования
            return Response({
                'cart_items': [],
                'total_price': 0}
            )

        cart_items = CartItem.objects.filter(user=request.user).select_related('product')
        total = sum([item.get_total_price() for item in cart_items])
        return Response({
            'cart_items': cart_items,
            'total_price': total
        })


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        #метод для ограничения доступа: каждый пользователь видит только свои товары в корзине
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # метод, отвечающий за создание нового CartItem, автоматически подставляя текущего пользователя
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs): #Получает элемент по его идентификатору с помощью self.get_object()
        try:
            instance = self.get_object()
            self.perform_destroy(instance) #метод perform_destroy удаляет элемент из базы данных.
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'error': 'Элемент не найден в корзине.'},
                            status=status.HTTP_404_NOT_FOUND
            )



#из-за CartHTMLDetailView этот класс не нужен, получается
class CartTotalView(APIView):
    #permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items = CartItem.objects.filter(user=request.user)
        total = sum([item.get_total_price() for item in items]) #item.get_total_price() —
        # метод модели, возвращающий price * quantity
        return  Response({'total_price': total})


#def cart_page(request):
    #cart_items = request.user.cart_items.select_related('product')
    #return render(request, 'cart.html') #! TODO rest frame применить,  permission_classes = [permissions.IsAuthenticated]
