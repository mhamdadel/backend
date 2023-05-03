from django.http import JsonResponse
from wishlist.models import Wishlist
from django.shortcuts import render
from ecommerce.models import Product
from authentication.models import CustomUser

def addToWish(request):
    if request.method=='POST':
        if request.CustomUser.is_authinticated:
          product_id=int(Product.POST.get('product_id'))
          product_check=Product.objects.get(id=product_id)
          if(product_check):
             if Wishlist.objects.filter(user=request.CustomUser.id, product_id=product_id):
                # Wishlist.objects.filter(user=request.CustomUser.id, product_id=product_id).delete()
                return JsonResponse({"status": "Product is already in the Wishlist"})
             else:
                Wishlist.objects.create(user=request.CustomUser.id, product_id=product_id)
        else:
           return JsonResponse({"status": "Not authenticated"})      

def getWishlist(request):
   if request.method=='GET':
      if request.CustomUser.is_authinticated:
         wishlist=Wishlist.objects.filter(user=request.CustomUser)
         return JsonResponse({"Wishlist": wishlist})
      else:
         return JsonResponse({"status": "Not authenticated"})

def deleteWishlist(request):
   if request.method=='DELETE':
      if request.CustomerUser.is_authenticated:
         product_id=int(request.GET('product_id'))
         if(Wishlist.objects.filter(user=request.CustomUser,product_id=product_id)):
            wishlistItem=Wishlist.objects.get(product_id=product_id)
            wishlistItem.delete()
            return JsonResponse({"status": "Product deleted"})
         else:
            return JsonResponse({"status": "Product not in the Wishlist"})
      else:
         return JsonResponse({"status": "Not authenticated"})
      
      
