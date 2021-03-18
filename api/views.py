from django.conf import settings
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from .serializers import OrderSerializer, ProductSerializer
from .models import Order, Product
from rest_framework import views, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, get_user_model
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import viewsets, status
import stripe
import json
from rest_framework import status

user = get_user_model()
stripe.api_key = settings.STRIPE_PRIVATE_KEY


class ProductListView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrdersListView(views.APIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


#Item addition to the card
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def add_item(request):
    print(request.data)
    id = request.data['id']
    product = Product.objects.get(id=id)
    if request.method == 'POST' and request.user != None:
        order = Order()
        order.product = product
        order.customer = request.user
        order.payed = False
        order.number = 1
        order.save()
        return Response({'message': "Ordered added to card"})
    elif product in Order.objects.filter(customer=request.user).all()[product]:
        return Response({'message': 'it exsist in your card'})
    else:
        return Response({'message': 'Error'})


#Displays orders
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def order_list(request):
    orders = Order.objects.filter(customer=request.user).all()
    serializer = OrderSerializer(orders, many=True)
    total = 0
    for order in orders:
        total += order.product.price
    if orders == None:
        return Response({'message': 'No orders yet'})

    return Response(data={'data': serializer.data, 'total': total})


#General checkout endpoint
@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def checkout(request):
    main_url = "http://localhost:3000"
    orders = Order.objects.filter(customer=request.user).all()
    total = 0
    for order in orders:
        total += order.product.price
    print(orders)
    if request.method == 'POST':
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(total),
                        'product_data': {
                            'name': orders[0].product.title,
                            'images': [orders[0].product.photo],
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=main_url + '/success',
            cancel_url=main_url + '/failed',
        )
        print(checkout_session.id)
        return Response(data={'id': checkout_session})
    if request.method == 'DELETE':
        orders = Order.objects.filter(customer=request.user).all()
        for order in orders:
            order.payed = True
            order.save()
        return Response({'message': "OK"})
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def removefromcard(request):
    print(request.data)
    order = Order.objects.filter(customer=request.user).filter(track_id=request.data['id'])
    order.delete()

    return Response(status=status.HTTP_200_OK)