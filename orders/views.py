from requests import request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from .models import Order
from cart.models import Cart
from authentication.models import CustomUser
from .serializers import OrderSerializer
# @login_required
# def order_list(request):
#     orders = Order.objects.filter(user=request.CustomUser)
#     return render(request, {'orders': orders})


# @login_required
# def order_list(request):
#     custom_user = get_object_or_404(CustomUser, email=request.user.email)
#     orders = Order.objects.filter(uid=custom_user)
#     return render(request, 'order_list.html', {'orders': orders})

# def order_list(request):
#     custom_user = get_object_or_404(CustomUser, email=request.user.email)
#     orders = Order.objects.filter(uid=custom_user)
#     data={'orders':list(orders.values())}
#     return JsonResponse(data)
    # return render(request, 'order_list.html', {'orders': orders})
# @login_required
@api_view()
def order_list(request):
    if request.user.is_authenticated:
        custom_user = CustomUser.objects.get(email=request.user.email)
        orders = Order.objects.filter(uid=custom_user)
        serializer = OrderSerializer(orders , many=True)
        return Response(serializer.data)
     
# def order_list(request):
#     if request.user.is_authenticated:
#         custom_user = CustomUser.objects.get(email=request.user.email)
#         orders = Order.objects.filter(uid=custom_user)
#         return render(request, {'orders': orders})
#     else:
#         return render(request, 'not authenticated')

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


