from ecommerce.models import Product
from wishlist.models import Wishlist
from rest_framework import serializers
from rest_framework.response import Response

class WishlistSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    user_id=serializers.IntegerField(read_only=True)
    product_id=serializers.IntegerField(read_only=True)

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