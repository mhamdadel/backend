from wishlist.serializers import WishlistSerializer
from wishlist.models import Wishlist
from ecommerce.models import Product
from authentication.models import CustomUser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.paginator import Paginator
      
@api_view(['GET','POST'])
def wishlist_crud(self,request):
   if request.method=='GET':
      if request.user.is_authenticated:
        custom_user=CustomUser.objects.get(email=request.user.email)
        wishlist=Wishlist.objects.filter(user_id=custom_user)
        serializer=WishlistSerializer(wishlist, many=True)
        paginated=Paginator(wishlist , 5)
        page_number=request.GET.get('page')
        page_obj=paginated.get_page(page_number)
        return Response({"data":serializer.data,"pagination":page_obj})
      else:
         return Response({"message":"User is not logged in"})
    
   if request.method=='POST':
         if request.user.is_authenticated:
           serializer = WishlistSerializer(data=request.data)
         #  serializer = WishlistSerializer(data=request.data, context={'request': request})
           if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
           else:
            return Response(serializer.errors)
         else:
           return Response({"message":"User is not logged in"})
         
   
@api_view('DELETE')
def wishlist_delete(request, id):
   if request.method=='DELETE':
         if request.user.is_authenticated:
            product_id=int(request.GET('product_id'))
            if(Wishlist.objects.filter(user=request.user,product_id=product_id)):
               wishlistItem=Wishlist.objects.get(product_id=product_id)
               wishlistItem.delete()
               return Response({"message": "Product deleted"})

         





