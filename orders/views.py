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
#         serializer = Order_ItemSerializer(data=request.data)
#         print(request.data)
#     if serializer.is_valid():
#          serializer.save()
#          return Response(serializer.data)
#     else:
#          return Response(serializer.errors)


# @api_view(['POST'])
# @permission_classes([is_auth])
# def add_order(request):
#                 user_id= get_user_id_from_token(request)
#                 # user = CustomUser.objects.get(id=user_id)
#                 order = Order.objects.create(uid=user_id)
#                 order = Order.objects.filter(uid=user_id).order_by('createdAt').first() or Order.objects.create(uid=user)  
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
    user = CustomUser.objects.get(id=user_id)
    shipping_address = request.data.get('shipping_address')
    phone_number = request.data.get('phone_number')
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

    cart = Cart.objects.get(user_id=user_id)
    cart_items = cart.cart_items.all()
    cart_items.delete()
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
    if(Order.objects.filter(uid=user_id)):
        if(OrderItem.objects.filter(id=order_id)):
          order = get_object_or_404(Order.objects, order_id=order_id, uid=user_id)
          serializer = OrderSerializer(order)
          return Response(serializer.get_order_items(order))
        else:
            return Response({'message':'Item not found'})


@permission_classes([is_auth])
@api_view(['post'])
def cancel_order(request, order_id):
    user_id = get_user_id_from_token(request)
    try:
        order = Order.objects.get(order_id=order_id, uid=user_id)
    except Order.DoesNotExist:
        return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    total_amount = order.get_total_amount() - 20
    cancellation_fees = order.get_cancellation_fees()
    order.status = 'Cancelled'
    order.cancellation_fees = cancellation_fees + 20
    order.save()
    data = {
        'total_amount': total_amount,
        'cancellation_fees': order.cancellation_fees,
    }
    return Response(data, status=status.HTTP_202_ACCEPTED)
 
 
@permission_classes([is_auth])
@api_view(['DELETE'])
def delete_order(request, order_id):
    print(order_id)
    user_id= get_user_id_from_token(request)
    try:
     order = Order.objects.get(order_id=order_id, uid=user_id)
    except Order.DoesNotExist:
        return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    order.delete()
    return Response({'message': 'Deleted Successfully'},status=status.HTTP_202_ACCEPTED)   

@permission_classes([is_auth])
def check_out(request, order_id):
    request.session['order_id']=order_id
    Cart.clear()
    return redirect(reverse('payment:process'))
