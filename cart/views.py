from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response

from order.views import OrderViewSet
from product.models import Product
from .models import CartItem
from .serializers import CartItemSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart_page')


@login_required(login_url='login_page')
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('cart_page')

    if request.method == 'POST':
        # вызываем OrderViewSet.create_from_cart
        view = OrderViewSet.as_view({'post': 'create_from_cart'})
        return view(request)

    return render(request, 'checkout.html', {'cart_items': cart_items})


class CartHTMLDetailView(APIView):
    """Представление для отображения корзины заказа конкретного пользователя в HTML."""
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated]
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

    def post(self, request):
        item_id = request.POST.get('remove_item')
        if item_id:
            CartItem.objects.filter(id=item_id, user=request.user).delete()
        return redirect('cart_page')


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items = CartItem.objects.filter(user=request.user)
        total = sum([item.get_total_price() for item in items]) #item.get_total_price() —
        # метод модели, возвращающий price * quantity
        return  Response({'total_price': total})


#def cart_page(request):
    #cart_items = request.user.cart_items.select_related('product')
    #return render(request, 'cart.html') #! TODO rest frame применить,  permission_classes = [permissions.IsAuthenticated]

