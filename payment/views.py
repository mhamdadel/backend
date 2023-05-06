from requests import request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# from django.utils import timezone
# from django.http import JsonResponse
from orders.models import Order
from .models import Payment
from backend.settings import PAYPAL_RECEIVER_EMAIL
from paypal.standard.forms import PayPalPaymentsForm
# from cart.models import Cart
from authentication.models import CustomUser
# from .serializers import OrderSerializer


@csrf_exempt
def payment_done(request):
    return render(request)


@csrf_exempt
def payment_canceled(request):
    return render(request)




def payment_process(request):
    order_id=request.session.get('order_id')
    order=get_object_or_404(Order, id=order_id)
    host= request.get_host()
    
    paypal_dict={
        'business': PAYPAL_RECEIVER_EMAIL,
        'amount' :Payment.amount ,
        'item_name' : 'Order{}'.format(Order.order_id),
        'invoice' : str(Order.order_id),
        'currency' : 'USD',
        'notify_url' : 'http://{}{}'.format(host,reverse('paypal-ipn')),
        'return_url' : 'http://{}{}'.format(host,reverse('payment:done')),
        'cancel_return' : 'http://{}{}'.format(host,reverse('payment:canceled')),
    }
    form=PayPalPaymentsForm(initial=paypal_dict)
    return render(request,{'order':order,'form':form})    

