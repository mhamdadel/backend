from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerilaizer(serializers.ModelSerializer):
    Category = CategorySerializer(many=False, read_only=True)

    class Meta: 
        model = Product
        # fileds = ['title','price','description', "image_url", "image", 'inStock']
        fields= '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # representation.pop("image")
        return representation