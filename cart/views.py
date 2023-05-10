import jwt
from cart.models import Cart,CartItem
from cart.serializers import CartItemSerializer,CartSerializer
from ecommerce.models import Product
from authentication.models import CustomUser
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.core.paginator import Paginator
from authentication.views import is_auth


@api_view()
@permission_classes([is_auth])
def cart(request):
    if request.method == 'GET':
         token = request.COOKIES.get('token')      
         decoded_token = jwt.decode(token, "PROJECT!@#%^2434", algorithms=["HS256"])
         user_id = decoded_token.get('user_id')        
      #   cart = Cart.objects.get(user=user_id)
         cart = Cart.objects.filter(user=user_id)
      #   serializer = CartSerializer(cart)
      #   paginated=Paginator(cart , 5)
      #   page_number=request.GET.get('page')
      #   page_obj=paginated.get_page(page_number)
      #   return Response({"data":serializer.data,"pagination":page_obj})
         paginated = Paginator(cart, 5)
         page_number = request.GET.get('page')
         page_obj = paginated.get_page(page_number)
         serializer = CartSerializer(page_obj, many=True)
         return Response({"data": serializer.data})  


# @api_view(['POST'])
# @permission_classes([is_auth])
# def add_to_cart(request,id):
#     if request.method == 'POST':
#             token = request.COOKIES.get('token')      
#             decoded_token = jwt.decode(token, "PROJECT!@#%^2434", algorithms=["HS256"])
#             user_id = decoded_token.get('user_id')   
#             product_id = request.POST.get('product_id')
#             product = Product.objects.get(id=product_id)
#             product_quantity = int(request.POST.get('product_quantity'))
#             if product:
#                 cart, created = Cart.objects.get_or_create(user=user_id)
#                 data={'id':id}
#                 cart_item, created = CartItem.objects.get_or_create(data=data,cart=cart, product=product)
#                #  if created:                   
#                 cart_item.quantity = product_quantity
#                 serializer = CartItemSerializer(cart_item)
#                 serializer.save()
#                 return Response(serializer.data, status=201)                   
#             # return Response(status=404)
#             else:
#              return Response({'message':"Product not found"})


@api_view(['POST'])
@permission_classes([is_auth])
def add_to_cart(request, id):
    if request.method == 'POST':
        token = request.COOKIES.get('token')      
        decoded_token = jwt.decode(token, "PROJECT!@#%^2434", algorithms=["HS256"])
        user_id = decoded_token.get('user_id')   
        product_id = request.POST.get('product_id')
        product_quantity = request.POST.get('product_quantity')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'message': "Product not found"}, status=404)
        if product:
            cart, created = Cart.objects.get_or_create(user=user_id)
            data = {'id': id}
            cart_item, created = CartItem.objects.get_or_create(data=data, cart=cart, product=product)
            cart_item.quantity = product_quantity
            serializer = CartItemSerializer(cart_item)
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response({'message': "Product not found"}, status=404)
              
         

@api_view(['DELETE','PUT'])
@permission_classes([is_auth])
def cart_item(request,id):
   if request.method == 'DELETE':
         token = request.COOKIES.get('token')      
         decoded_token = jwt.decode(token, "PROJECT!@#%^2434", algorithms=["HS256"])
         user_id = decoded_token.get('user_id')            
         # product_id=int(request.GET('product_id'))
         if(Cart.objects.filter(user=user_id)):
           if(CartItem.objects.filter(id=id)):
            cart_item = CartItem.objects.get(id=id)
            cart_item.delete()
            return Response({'message':'Item Deeleted Successfully'})
           else:
            return Response({'message':'Item not found'})

    
   if request.method=='PUT':
         token = request.COOKIES.get('token')      
         decoded_token = jwt.decode(token, "PROJECT!@#%^2434", algorithms=["HS256"])
         user_id = decoded_token.get('user_id')  
         # serializer=CartItemSerializer(request.data)
        #  product_id = int(request.data.get('product_id'))
         if(Cart.objects.filter(user=user_id)):
          cart_item = CartItem.objects.get(id=id)
          serializer = CartItemSerializer(cart_item, data=request.data)
          if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
          else:
            return Response(serializer.errors)







    
