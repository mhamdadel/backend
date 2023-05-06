from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.authtoken.models import Token
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        # fields = ['email', 'password', 'password2', 'first_name', 'last_name', 'phone_number', 'city','state', 'zip_code', 'country', 'date_joined','last_login', 'is_staff', 'is_active', 'is_super']
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'phone_number': {'required': True},
        }

    def validate_first_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('First name must be at least 2 characters long.')
        return value

    def validate_last_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('Last name must be at least 2 characters long.')
        return value

    def validate_phone_number(self, value):
        if len(value) < 10:
            raise serializers.ValidationError('Phone number must be at least 10 digits long.')
        if len(value) > 15:
            raise serializers.ValidationError('Phone number must be at most 15 digits long.')
        return value

    def validate(self, data):
        email = data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email address is already in use.')
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Passwords do not match.')
        return data

    def create(self, validated_data):
        validated_data['password'] = hash_password(validated_data['password'])
        print("asd", validated_data)
        validated_data.pop('password2', None)  # Remove password2 field from validated_data
        user = CustomUser(**validated_data)
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, data):
        email = data.get('email')
        password = hash_password(data.get('password'))
        if email and password:
            user = CustomUser.objects.get(email=email)
            print("why : ",user.password, password)
            if not user:
                raise AuthenticationFailed('Invalid email or password')
            if not user.is_active:
                raise AuthenticationFailed('User account is disabled')
            if user.password != password:
                raise AuthenticationFailed('Invalid email or password')
            token, _ = Token.objects.get_or_create(user=user)
            return {'user': user, 'token': token.key}
        else:
            raise ValidationError('Must include "email" and "password".')
    
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=False)
    class Meta:
        model = CustomUser
        # fields = ['id', 'email', 'username', 'first_name', 'last_name', 'phone_number', 'password', 'password2']
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True},
            'phone_number': {'required': True},
        }

    def validate_first_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('First name must be at least 2 characters long.')
        return value

    def validate_last_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('Last name must be at least 2 characters long.')
        return value

    def validate_phone_number(self, value):
        if len(value) < 10:
            raise serializers.ValidationError('Phone number must be at least 10 digits long.')
        if len(value) > 15:
            raise serializers.ValidationError('Phone number must be at most 15 digits long.')
        return value

    def validate(self, data):
        if 'view' in self.context:
            view = self.context['view']
            if hasattr(view, 'action') and view.action == 'create':
                if CustomUser.objects.filter(email=data['email']).exists():
                    raise serializers.ValidationError('Email address is already in use.')
                if data['password'] != data.get('password2'):
                    raise serializers.ValidationError('Passwords do not match.')
                validate_password(data['password'], user=CustomUser(**data))
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        return super().update(instance, validated_data)
    

    from rest_framework import generics, permissions, status
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .models import CustomUser
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
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = AccessToken.for_user(user)
        response = Response({
            "token": str(token),
            "user": serializer.data,
        })
        response.set_cookie("token", str(token), httponly=True)
        response.set_cookie("user", serializer.data, httponly=True)
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

class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
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