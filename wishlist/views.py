import jwt
from wishlist.serializers import WishlistSerializer
from wishlist.models import Wishlist
from ecommerce.models import Product
from authentication.models import CustomUser
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.core.paginator import Paginator
from authentication.views import is_auth
      

@api_view(['GET','POST'])
# @permission_classes([is_auth])
def wishlist_crud(request):
   if request.method=='GET':
      #   token=request.COOKIES.get('token')
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

# def wishlist_crud(request):
#    if request.method == 'GET':
#         token = request.COOKIES.get('token')
#         if token:
#             decoded_token = jwt.decode(token, "PROJECT!@#%^2434", algorithms=["HS256"])
#             user_id = decoded_token['user_id']
#             custom_user = CustomUser.objects.get(id=user_id)
#             wishlist = Wishlist.objects.filter(user_id=custom_user.id).order_by('id')            
#             serializer = WishlistSerializer(wishlist, many=True)
#             paginated = Paginator(wishlist, 5)
#             page_number = request.GET.get('page')
#             page_obj = paginated.get_page(page_number)
#             return Response({"data": serializer.data, "pagination":page_obj})
#         else:
#          decoded_token = jwt.decode(token, "PROJECT!@#%^2434", "HS256")
#          return Response(token)

    
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
   
# @api_view(['DELETE'])
# def wishlist_delete(request, id):
#    if request.method=='DELETE':
#          if request.user.is_authenticated:
#             # product_id=int(request.GET('product_id'))
#             product_id = int(request.GET['product_id'])
#             if(Wishlist.objects.filter(user=request.user,product_id=product_id)):
#                wishlistItem=Wishlist.objects.get(product_id=product_id)
#                wishlistItem.delete()
#                return Response({"message": "Product deleted"})

@api_view(['DELETE'])
# @permission_classes([is_auth])
def wishlist_delete(request):
   if request.method == 'DELETE':
         token=request.COOKIES.get('token')
      # if token.is_authenticated:
         product_id = int(request.GET['product_id'])
         if Wishlist.objects.filter(user=token.user, product_id=product_id).exists():
            wishlist_item = Wishlist.objects.get(user=request.user, product_id=product_id)
            wishlist_item.delete()
            return Response({"message": "Product deleted"})
         else:
            return Response({"message": "Product not found"})
      # else:
      #    return Response({"message": "User not authenticated"})



         





