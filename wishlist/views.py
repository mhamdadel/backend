import jwt
from wishlist.serializers import WishlistSerializer
from wishlist.models import Wishlist
from ecommerce.models import Product
from authentication.models import CustomUser
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.core.paginator import Paginator
from authentication.views import is_auth
      

@api_view()
@permission_classes([is_auth])
def wishlist_view(request):
   if request.method == 'GET':
            token = request.COOKIES.get('token')      
            decoded_token = jwt.decode(token, "PROJECT!@#%^2434", algorithms=["HS256"])
            user_id = decoded_token.get('user_id')
            wishlist = Wishlist.objects.filter(user_id=user_id).order_by('id').select_related('product_id')
            wishlist_items=wishlist.all().order_by('id');      
            paginated = Paginator(wishlist_items, per_page=1)
            page_number = request.GET.get('page')
            page_obj = paginated.get_page(page_number)
            serializer = WishlistSerializer(page_obj, many=True)
            response_data = {
            "data": serializer.data,
            "total_pages": paginated.num_pages,
            "current_page": page_number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous()
        }
            return Response(response_data)
            # return Response({"data": serializer.data})            

@api_view(['POST'])
@permission_classes([is_auth])
def wishlist_add(request):
 if request.method=='POST':
         id=request.data.get('id')
         data = {'product_id': id}
         serializer = WishlistSerializer(data=data, context={'request': request})  
         if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
         else:
             return Response(serializer.errors)



@api_view(['DELETE'])
@permission_classes([is_auth])
def wishlist_delete(request, id):
    if request.method == 'DELETE':
        token = request.COOKIES.get('token')
        decoded_token = jwt.decode(token, "PROJECT!@#%^2434", algorithms=["HS256"])
        user_id = decoded_token.get('user_id')
      #   try:
        if Wishlist.objects.filter(user_id=user_id,id=id).exists():
            wishlist_item = Wishlist.objects.get(id=id, user_id=user_id)
            wishlist_item.delete()
            return Response({"message": "Product deleted"})
      #   except Wishlist.DoesNotExist:
        else:
            return Response({"message": "Product not found"})

         





