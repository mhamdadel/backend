from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from orders.serializers import OrderSerializer
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .models import CustomUser
from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer, CartSerializer
from wishlist.serializers import WishlistSerializer
import jwt

class NotAuthenticatedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return not jwt.decode(request.COOKIES.get('token'), "PROJECT!@#%^2434", "HS256").get('user_id')
        except Exception as e:
            return True
    
class is_auth(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return jwt.decode(request.COOKIES.get('token'), "PROJECT!@#%^2434", "HS256").get('user_id')
        except Exception as e:
            return False
    
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [NotAuthenticatedPermission]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user : 
            cartForNewUser = Cart(user_id=user.id)
            cartForNewUser.save()
        token = AccessToken.for_user(user)
        theUser = LoginSerializer(user, context=self.get_serializer_context()).data
        response = Response({
            "token": str(token),
            "user": theUser,
        })
        response.set_cookie("token", str(token), httponly=True)
        response.set_cookie("user", theUser, httponly=True)
        return response


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [NotAuthenticatedPermission]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = AccessToken.for_user(user)
        theUser = LoginSerializer(user, context=self.get_serializer_context()).data
        response = Response({
            "token": str(token),
            "user": theUser,
        })
        response.set_cookie("token", str(token), max_age=7*24*60*60, httponly=True)
        response.set_cookie("user", theUser, max_age=7*24*60*60, httponly=True)
        return response

class LogoutAPI(generics.GenericAPIView):
    permission_classes = [is_auth]

    def post(self, request, *args, **kwargs):
        try:
            response = Response({
                "message": "Successfully logged out"
            })
            response.delete_cookie("token")
            response.delete_cookie("user")
            return response
        except AttributeError:
            pass

class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [is_auth]

    def get_object(self):
        userId = jwt.decode(self.request.COOKIES.get('token'), "PROJECT!@#%^2434", "HS256").get('user_id')
        user = CustomUser.objects.get(id=userId)
        return user

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.validate(request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password')
        if password:
            instance.set_password(password)
        serializer.save()
        # add any additional data to the response
        response_data = {
            'user': serializer.data,
            'message': 'Account details updated successfully.'
        }
        return Response(response_data)
    
class MyOrders(generics.GenericAPIView):
    permission_classes = [is_auth]
    def get(self, request, *args):
        myId = jwt.decode(request.COOKIES.get('token'), "PROJECT!@#%^2434", "HS256").get('user_id')
        user = CustomUser.objects.get(id=myId)
        orders = user.orders.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
class MyOrderDetails(generics.GenericAPIView):
    permission_classes = [is_auth]
    def get(self, request, id):
        myId = jwt.decode(request.COOKIES.get('token'), "PROJECT!@#%^2434", "HS256").get('user_id')
        user = CustomUser.objects.get(id=myId)
        orders = user.orders.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data[0])
    
class MyWishListItems(generics.GenericAPIView):
    permission_classes = [is_auth]
    def get(self, request, *args):
        myId = jwt.decode(request.COOKIES.get('token'), "PROJECT!@#%^2434", "HS256").get('user_id')
        user = CustomUser.objects.get(id=myId)
        wishListItems = user.wishlist.all()
        serializer = WishlistSerializer(wishListItems, many=True)
        return Response(serializer.data)

class MyCart(generics.GenericAPIView):
    permission_classes = [is_auth]
    def get(self, request, *args):
        myId = jwt.decode(request.COOKIES.get('token'), "PROJECT!@#%^2434", "HS256").get('user_id')
        user = CustomUser.objects.get(id=myId)
        cartItems =  user.cart.cart_items.all()
        # cart = Cart.objects.get(user=user)
        # cartItems = CartItem.objects.get(cart=cart)
        serializer = CartItemSerializer(cartItems, many=True)
        print ()
        # ser = CartSerializer(Cart.objects.get(user_id=myId), many=False)
        return Response(serializer.data)
        # return Response(serializer.data)

