from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import RegisterSerializer, LoginSerializer

class NotAuthenticatedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated
    
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [NotAuthenticatedPermission]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = AccessToken.for_user(user)
        print(token)
        return Response({
            "token": str(token),
            "user": LoginSerializer(user, context=self.get_serializer_context()).data,
        }).set_cookie({
            "token": str(token),
            "user": LoginSerializer(user, context=self.get_serializer_context()).data,
        }, httponly=True)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [NotAuthenticatedPermission]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = AccessToken.for_user(user)
        return Response({
            "token": str(token),
            "user": LoginSerializer(user, context=self.get_serializer_context()).data,
        }).set_cookie({
            "token": str(token),
            "user": LoginSerializer(user, context=self.get_serializer_context()).data,
        }, httponly=True)

class LogoutAPI(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            request.auth.delete()
        except AttributeError:
            pass
        return Response({
            "message": "Successfully logged out"
        })