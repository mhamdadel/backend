from ecommerce.serializers import ProductSerilaizer
import jwt
from cart.models import Cart,CartItem
from cart.serializers import CartItemSerializer,CartSerializer
from ecommerce.models import Product
from authentication.models import CustomUser
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.core.paginator import Paginator
from authentication.views import is_auth


# @api_view()
# @permission_classes([is_auth])
# def cart(request):
#     if request.method == 'GET':
#          token = request.COOKIES.get('token')      
#          decoded_token = jwt.decode(token, "PROJECT!@#%^2434", algorithms=["HS256"])
#          user_id = decoded_token.get('user_id')        
#          cart = Cart.objects.filter(user=user_id).order_by('cart_items')
#          p= Paginator(cart,2)
#          page = request.GET.get('page')
#          carts = p.get_page(page)
#          serializer = CartSerializer(carts , many=True, context={'request': request})
#          return Response(serializer.data)

@api_view(['GET'])
@permission_classes([is_auth])
def cart(request):
    if request.method == 'GET':
        token = request.COOKIES.get('token')      
        decoded_token = jwt.decode(token, "PROJECT!@#%^2434", algorithms=["HS256"])
        user_id = decoded_token.get('user_id')        
        cart = Cart.objects.filter(user=user_id).first()
        cart_items = cart.cart_items.all().order_by('id')
        paginator = Paginator(cart_items, 2)
        page = request.GET.get('page')
        cart_items_paginated = paginator.get_page(page)
        serializer = CartItemSerializer(cart_items_paginated, many=True, context={'request': request})
        return Response({'cart_items': serializer.data})

@api_view(['POST'])
@permission_classes([is_auth])
def add_to_cart(request):
    if request.method == 'POST':
        token = request.COOKIES.get('token')      
        decoded_token = jwt.decode(token, "PROJECT!@#%^2434", algorithms=["HS256"])
        user_id = decoded_token.get('user_id')
        id=request.data.get('id')
        product = Product.objects.get(id=id)
        instock=product.inStock
        instock=instock-1
        product.inStock = instock  
        product.save() 
        if product:
            cart, created = Cart.objects.get_or_create(user=user_id)
            serializer = CartItemSerializer(data={'cart': cart, 'product': id, 'quantity': 1}, context={'request': request, 'cart': cart, 'method': request.method})
            # cart_item.quantity = quantity
            # product_dict = ProductSerilaizer(product).data
            # # print(product_dict['id'])
            # serializer = CartItemSerializer(data={'cart': cart, 'product': product_dict, 'quantity': quantity}, context={'request': request, 'cart': cart, 'method': request.method})
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
            product = Product.objects.get(id=cart_item.product.id)
            print(request.data)
            quantity=request.data.get('quantity')
            quantity=int(quantity)
            print(quantity)
            if(quantity>cart_item.quantity):
              instock=product.inStock
              instock=instock-quantity
              product.inStock = instock  
              product.save() 
            else:
              instock=product.inStock
              instock=instock+quantity
              product.inStock = instock  
              product.save()           
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

             
             







    
