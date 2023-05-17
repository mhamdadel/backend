from requests import request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.utils import timezone
from authentication.views import is_auth
from .models import Order, OrderItem
from cart.models import Cart
from authentication.views import is_auth
from authentication.models import CustomUser
from .serializers import Order_ItemSerializer, OrderSerializer
from ecommerce.models import Product
import jwt


def get_user_id_from_token(request):
    token = request.COOKIES.get('token')
    decoded_token = jwt.decode(token , "PROJECT!@#%^2434" , algorithms=["HS256"])
    user_id = decoded_token.get('user_id')
    return user_id

@api_view()
@permission_classes([is_auth])
def order_list(request):        
    user_id= get_user_id_from_token(request)
    orders = Order.objects.filter(uid=user_id)
    p = Paginator(orders,100)
    page = request.GET.get('page')
    orderss = p.get_page(page)
    serializer = OrderSerializer(orderss , many=True)
    return Response(serializer.data)
     

# @api_view(['POST'])
# # @permission_classes([is_auth])
# def add_order(request):
#     #  user_id= get_user_id_from_token(request)
#     #  order = Order.objects.get_or_create(uid=user_id)
#      serializer = Order_ItemSerializer(data=request.data)
#      if serializer.is_valid():
#          serializer.save()
#          return Response(serializer.data)
#      else:
#          return Response(serializer.errors)


# @api_view(['POST'])
# # @permission_classes([is_auth])
# def add_order(request):
#     if request.method == 'POST':
#         # user_id = get_user_id_from_token(request)
#         # orders = Order.objects.filter(uid=user_id)
#         print (request.data)
#         #  ['order','product', 'quantity', 'price']
#         # address / phone / cart data 
#         # product_id = product # product = product_id
        
#         # create order
#         # order _id 
#         # insert in order [items = cart_data]
#         serializer = Order_ItemSerializer(data=request.data)
#     if serializer.is_valid():
#          serializer.save()
#          return Response(serializer.data)
#     else:
#         print('error')
#         return Response(serializer.errors)


# @api_view(['POST'])
# @permission_classes([is_auth])
# def add_order(request):
#                 user_id= get_user_id_from_token(request)
#                 # user = CustomUser.objects.get(id=user_id)
#                 order = Order.objects.create(uid=user_id)
#                 # order = Order.objects.filter(uid=user_id).order_by('createdAt').first() or Order.objects.create(uid=user_id)  
#                 print(order)
                
#                 order_item = OrderItem.objects.create(order=order)
#                 print(order_item)
#                 serializer = Order_ItemSerializer(order_item)
#                 serializer.save()
#                 return Response(serializer.data, status=201)                   
              
@api_view(['POST'])
@permission_classes([is_auth])
def add_order(request):
    user_id = get_user_id_from_token(request)
    shipping_address = request.data.get('shipping_address')
    phone_number = request.data.get('phone_number')
    print("#############################################")
    print(request.data.get('cart_data'))
    cart_data = request.data.get('cart_data')[0]

    order = Order.objects.create(uid_id=user_id, shipping_address=shipping_address, phone_number=phone_number, status="pending")
    order_serializer = OrderSerializer(order)

    order_items = []
    for item in cart_data:
        product_id = item['product_id']
        quantity = item['quantity']
        price = item['price']

        product = Product.objects.get(id=product_id)
        order_item = OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
        order_item.save()

        order_items.append(order_item)

    order_item_serializer = Order_ItemSerializer(order_items, many=True)
    response_data = {
        'order': order_serializer.data,
        'order_items': order_item_serializer.data,
    }
    return Response(response_data, status=status.HTTP_201_CREATED)




# @api_view(['POST'])
# @permission_classes([is_auth])
# def add_order(request):
#      serializer = OrderSerializer(data=request.data)
#      if serializer.is_valid():
#          serializer.save() 
#          return Response(serializer.data)
#      else:
#          return Response(serializer.errors)




@api_view()
@permission_classes([is_auth])
def order_detail(request, order_id):
    
    user_id= get_user_id_from_token(request)
    # custom_user = CustomUser.objects.get(email=request.user.email)
    # order = get_object_or_404(Order, order_id=order_id, uid=user_id)
    order = get_object_or_404(Order.objects, order_id=order_id, uid=user_id)
    serializer = OrderSerializer(order)
    return Response(serializer.get_order_items(order))


@permission_classes([is_auth])
def cancel_order(request, order_id):
    
    user_id= get_user_id_from_token(request)
    order = get_object_or_404(Order, id=order_id, uid=user_id)
    serializer = OrderSerializer(order)
    if order.status != 'PENDING':
        return Response(serializer.data)
    if timezone.now() > order.createdAt + timezone.timedelta(days=2):
            order.delete()
    

@permission_classes([is_auth])
def check_out(request, order_id):
    request.session['order_id']=order_id
    Cart.clear()
    return redirect(reverse('payment:process'))


