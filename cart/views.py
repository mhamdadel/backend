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
         cart = Cart.objects.filter(user=user_id)
         p= Paginator(cart,5)
         page = request.GET.get('page')
         carts = p.get_page(page)
         serializer = CartSerializer(carts , many=True)
         return Response(serializer.data)

@api_view(['POST'])
@permission_classes([is_auth])
def add_to_cart(request, product_id):
    if request.method == 'POST':
        token = request.COOKIES.get('token')      
        decoded_token = jwt.decode(token, "PROJECT!@#%^2434", algorithms=["HS256"])
        user_id = decoded_token.get('user_id')  
        quantity =request.data.get('quantity')
        if quantity is not None:
            quantity = int(quantity)
        product = Product.objects.get(id=product_id)
        if product:
            cart, created = Cart.objects.get_or_create(user=user_id)
            serializer = CartItemSerializer(data={'cart': cart, 'product': product_id, 'quantity': quantity}, context={'request': request, 'cart': cart, 'method': request.method})
            # cart_item.quantity = quantity
            if serializer.is_valid():
               serializer.save()
               return Response(serializer.data, status=201)
            else:
               return Response(serializer.errors)
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
        if Cart.objects.filter(user=user_id).exists():
          if CartItem.objects.filter(id=id).exists():
            cart_item = CartItem.objects.select_related('cart', 'product').get(id=id)
            serializer= CartItemSerializer(cart_item, data=request.data, context={'request': request, 'method': request.method})
            # print(cart_item.product)
            # print(request.data)
            if serializer.is_valid():
              serializer.save(cart=cart_item.cart, product=cart_item.product)           
              return Response(serializer.data)
            else:
              return Response(serializer.errors)
          else:
            return Response("Cart Item doesn't exist")

             
             







    
