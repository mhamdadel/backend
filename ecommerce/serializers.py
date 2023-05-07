from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class ProductSerilaizer(serializers.ModelSerializer):


    class Meta: 
        model = Product
        fileds = ['title','price','description', "image_url", "image", 'inStock']


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("image")
        return representation