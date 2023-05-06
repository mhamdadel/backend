from ecommerce.models import Product
from cart.models import CartItem,Cart
from rest_framework import serializers

class CartSerializer(serializers.Serializer):
    id=serializers.IntegerField();
    user=serializers.IntegerField();
    



class CartItemSerializer(serializers.Serializer):
    id=serializers.IntegerField();
    cart=serializers.IntegerField();
    product=serializers.IntegerField();
    quantity=serializers.IntegerField();

    def validate(self, data):
        user_id = data.get('user_id')
        # user_id = self.context['request'].user.id
        product_id = data.get('product_id')
        
        product_check = Product.objects.filter(id=product_id).exists()
        if not product_check:
            raise serializers.ValidationError("Product does not exist")
        
        if CartItem.objects.filter(user_id=user_id, product_id=product_id).exists():
            raise serializers.ValidationError("Product is already in the Cart")
        # data['user_id'] = user_id
        return data

    def create(self,validated_data):
        return CartItem.objects.create(**validated_data);
     
    def update(self, instance, validated_data):
        instance.quantity=validated_data.get('quantity');
        instance.save();
        return instance;