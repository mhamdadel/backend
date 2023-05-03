from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import RegisterSerializer, LoginSerializer
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [NotAuthenticatedPermission]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
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
    authentication_classes = [JWTAuthentication]
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
        response.set_cookie("token", str(token), httponly=True)
        response.set_cookie("user", theUser, httponly=True)
        return response

class LogoutAPI(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
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