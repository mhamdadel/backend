from django.http import JsonResponse
from cart.models import Cart,CartItem
from ecommerce.models import Product
from django.shortcuts import render
from authentication.models import CustomUser
def add_to_cart(request):
    if request.method == 'POST':
        if request.CustomUser.is_authenticated:
            product_id=int(request.POST.get('product_id'))
            product=Product.objects.get(id=product_id)
            product_quantity = int(request.POST.get('product_quantity'))
            if product:
             cart, created=Cart.objects.get_or_create(user=request.CustomUser)
             cart_item, created=CartItem.objects.get_or_create(cart=cart,product=product)
             cart_item.quantity=product_quantity
             cart_item.save();
             return JsonResponse({'status':"Product added successfully"})
            else:
               return JsonResponse({'status':"Product not found"})
        else:
           return JsonResponse({'status':"You are not logged in"})
           

                 


    

            


