from requests import request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import JsonResponse
from .models import Order
from cart.models import Cart
from authentication.views import is_auth
from authentication.models import CustomUser
from .serializers import Order_ItemSerializer, OrderSerializer

# @login_required
@api_view()
@permission_classes([is_auth])
def order_list(request):
    custom_user = CustomUser.objects.get(email=request.user.email)
    orders = Order.objects.filter(uid=custom_user)
    p = Paginator(orders,3)
    page = request.GET.get('page')
    orderss = p.get_page(page)
    serializer = OrderSerializer(orderss , many=True)
    return Response(serializer.data)
     

@api_view(['POST'])
@permission_classes([is_auth])
def add_order(request):
     serializer = Order_ItemSerializer(data=request.data)
     if serializer.is_valid():
         serializer.save()
         return Response(serializer.data)
     else:
         return Response(serializer.errors)

# @login_required
@api_view()
@permission_classes([is_auth])
def order_detail(request, order_id):
    custom_user = CustomUser.objects.get(email=request.user.email)
    order = get_object_or_404(Order, id=order_id, uid=custom_user)
    serializer = Order_ItemSerializer(order)
    return Response(serializer.data)

# @login_required
@permission_classes([is_auth])
def cancel_order(request, order_id):
    custom_user = CustomUser.objects.get(email=request.user.email)
    order = get_object_or_404(Order, id=order_id, uid=custom_user)
    serializer = OrderSerializer(order)
    if order.status != 'PENDING':
        return Response(serializer.data)
    if timezone.now() > order.createdAt + timezone.timedelta(days=2):
        return Response(serializer.data)
    
    order.delete()

@permission_classes([is_auth])
def check_out(request, order_id):
    request.session['order_id']=order_id
    Cart.clear()
    return redirect(reverse('payment:process'))


