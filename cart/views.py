from cart.models import Cart,CartItem
from cart.serializers import CartItemSerializer,CartSerializer
from ecommerce.models import Product
from authentication.models import CustomUser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.paginator import Paginator


@api_view()
def cart(self, request):
    if request.method == 'GET':
      if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        serializer = CartSerializer(cart)
        paginated=Paginator(cart , 5)
        page_number=request.GET.get('page')
        page_obj=paginated.get_page(page_number)
        return Response({"data":serializer.data,"pagination":page_obj})
        # return Response(serializer.data)
      else:
       return Response({"message":"You are not logged in"})


api_view('POST')
def add_to_cart(self, request):
    if request.method == 'POST':
      #   custom_user = CustomUser.objects.get(email=request.user.email)
        if request.CustomUser.is_authenticated:
            product_id = int(request.POST.get('product_id'))
            product = Product.objects.get(id=product_id)
            product_quantity = int(request.POST.get('product_quantity'))
            if product:
                cart, created = Cart.objects.get_or_create(user=request.CustomUser)
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
               #  if created:                   
                cart_item.quantity = product_quantity
                serializer = CartItemSerializer(cart_item)
                serializer.save()
                return Response(serializer.data, status=201)                   
            # return Response(status=404)
            else:
             return Response({'message':"Product not found"})
        else:
           return Response({'message':"User not logged in"})
              
         

api_view(['DELETE','PUT'])
def cart_item(self, request):
   if request.method == 'DELETE':
      if request.user.is_authenticated:
         product_id=int(request.GET('product_id'))
         if(CartItem.objects.filter(user=request.user,product_id=product_id)):
            cart_item = CartItem.objects.get(user=request.user,product_id=product_id)
            cart_item.delete()
            return Response({'message':'Item Deeleted Successfully'})
         else:
            return Response({'message':'Item not found'})
      else:
         return Response({'message':'User not logged in'})
    
   if request.method=='PUT':
      if request.user.is_authenticated:
         serializer=CartItemSerializer(request.data)
        #  product_id = int(request.data.get('product_id'))
        #  cart_item = CartItem.objects.get(cart_user=request.user, product_id=product_id)
        #  serializer = CartItemSerializer(cart_item, data=request.data)
         if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
         else:
            return Response(serializer.errors)
      else:
         return Response({'message':'User not logged in'})






    
