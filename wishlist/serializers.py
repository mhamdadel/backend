import jwt
from ecommerce.serializers import ProductSerilaizer
from ecommerce.models import Product
from wishlist.models import Wishlist
from rest_framework import serializers
from rest_framework.response import Response
from authentication.serializers import UserSerializer
from authentication.models import CustomUser
import json


class WishlistSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    user_id= serializers.PrimaryKeyRelatedField(read_only=True)
    # product_id=ProductSerilaizer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    def validate(self, data):
        request = self.context.get('request')
        token = request.COOKIES.get('token')
        decoded_token = jwt.decode(token, "PROJECT!@#%^2434", algorithms=["HS256"])
        user_id = decoded_token.get('user_id')
        # product_id = data.get('product_id').get('id')
        product_id = data.get('product_id').id


        print(product_id)
        product_check = Product.objects.filter(id=product_id).exists()
        if not product_check:
            raise serializers.ValidationError("Product does not exist")
        if Wishlist.objects.filter(user_id=user_id, product_id=product_id).exists():
            raise serializers.ValidationError("Product is already in the Wishlist")
        data['user_id'] = CustomUser.objects.get(id=user_id)
        return data

    def create(self, validated_data):
        return Wishlist.objects.create(**validated_data)
        # product_data = validated_data.pop('product_id')
        # product_id = Product.objects.get(id=product_data['id'])
        # validated_data['product_id'] = product_id
        # return Wishlist.objects.create(product_id=product_id, **validated_data)