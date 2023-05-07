from ecommerce.models import Product
from wishlist.models import Wishlist
from rest_framework import serializers
from rest_framework.response import Response
from authentication.serializers import UserSerializer
from authentication.models import CustomUser

class WishlistSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    user_id=serializers.IntegerField(read_only=True)
    product_id=serializers.IntegerField(read_only=True)

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     custom_user = CustomUser.objects.get(id=data['user_id'])
    #     custom_user_serializer = UserSerializer(custom_user)
    #     data['user'] = custom_user_serializer.data
    #     data['user_id'] = custom_user_serializer.data['id']
    #     return data

    def validate(self, data):
        user_id = data.get('user_id')
        # user_id = self.context['request'].user.id
        product_id = data.get('product_id')
        
        product_check = Product.objects.filter(id=product_id).exists()
        if not product_check:
            raise serializers.ValidationError("Product does not exist")
        
        if Wishlist.objects.filter(user_id=user_id, product_id=product_id).exists():
            raise serializers.ValidationError("Product is already in the Wishlist")
        # data['user_id'] = user_id
        return data

    def create(self, validated_data):
        return Wishlist.objects.create(**validated_data)