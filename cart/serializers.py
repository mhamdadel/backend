import jwt
from authentication.models import CustomUser
from ecommerce.models import Product
from cart.models import CartItem,Cart
from rest_framework import serializers

class CartSerializer(serializers.Serializer):
    id=serializers.StringRelatedField();
    user=serializers.StringRelatedField(read_only=True);
    # cart=CartItemSerializer();

class CartItemSerializer(serializers.Serializer):
    id=serializers.StringRelatedField();
    cart=serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all());
    product=serializers.PrimaryKeyRelatedField(queryset=Product.objects.all());
    quantity=serializers.IntegerField();


    # def validate(self, data):
    #     request = self.context.get('request')
    #     token = request.COOKIES.get('token')
    #     decoded_token = jwt.decode(token, "PROJECT!@#%^2434", algorithms=["HS256"])
    #     user_id= decoded_token.get('user_id')
    #     # product_id = data.get('product_id').get('id')
    #     product= data.get('product_id').id
    #     cart= data.get('cart').id
    #     print(product)
    #     product_check = Product.objects.filter(id=product).exists()
    #     if not product_check:
    #         raise serializers.ValidationError("Product does not exist")
    #     if Cart.objects.filter(user=user_id,id=cart):
    #      if CartItem.objects.filter(id=id).exists():
    #         raise serializers.ValidationError("Product is already in the Wishlist")
    #     # data['user_id'] = CustomUser.objects.get(id=user_id)
    #     return data
   
    def validate(self, data):
        request = self.context.get('request')
        token = request.COOKIES.get('token')
        decoded_token = jwt.decode(token, "PROJECT!@#%^2434", algorithms=["HS256"])
        user_id = decoded_token.get('user_id')
        product = data.get('product').id
        print(product)
        cart = data.get('cart').id
        product_check = Product.objects.filter(id=product).exists()
        if not product_check:
            raise serializers.ValidationError("Product does not exist")
        if Cart.objects.filter(user=user_id, id=cart):
            if CartItem.objects.filter(product=product, cart=cart).exists():
                raise serializers.ValidationError("Product is already in the cart")
        return data

    def create(self,validated_data):
        return CartItem.objects.create(**validated_data);
     
    def update(self, instance, validated_data):
        instance.quantity=validated_data.get('quantity');
        instance.save();
        return instance;


# class CartSerializer(serializers.Serializer):
#     id=serializers.StringRelatedField();
#     user=serializers.StringRelatedField();
#     # cart=CartItemSerializer();