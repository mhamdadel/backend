from requests import request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import JsonResponse
from .models import Order
from cart.models import Cart
from authentication.models import CustomUser
from .serializers import OrderSerializer

# @login_required
@api_view()
def order_list(request):
    if request.user.is_authenticated:
        custom_user = CustomUser.objects.get(email=request.user.email)
        orders = Order.objects.filter(uid=custom_user)
        p = Paginator(orders,3)
        page = request.GET.get('page')
        orderss = p.get_page(page)
        serializer = OrderSerializer(orderss , many=True)
        return Response(serializer.data)
     

# @login_required
@api_view()
def order_detail(request, order_id):
 if request.user.is_authenticated:
    custom_user = CustomUser.objects.get(email=request.user.email)
    order = get_object_or_404(Order, id=order_id, uid=custom_user)
    serializer = OrderSerializer(order)
    return Response(serializer.data)

# @login_required
def cancel_order(request, order_id):
    custom_user = CustomUser.objects.get(email=request.user.email)
    order = get_object_or_404(Order, id=order_id, uid=custom_user)
    serializer = OrderSerializer(order)
    if order.status != 'PENDING':
        return Response(serializer.data)
    if timezone.now() > order.createdAt + timezone.timedelta(days=2):
        return Response(serializer.data)
    
    order.delete()


def check_out(request, order_id):
    request.session['order_id']=order_id
    Cart.clear()
    return redirect(reverse('payment:process'))


