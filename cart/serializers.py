from ecommerce.serializers import ProductSerilaizer
from ecommerce.models import Product
from cart.models import CartItem,Cart
from rest_framework import serializers

class CartItemSerializer(serializers.Serializer):
    id=serializers.StringRelatedField();
    cart=serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all(),required=False)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)
    product_details = serializers.SerializerMethodField(read_only=True)
    quantity=serializers.IntegerField();


    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'product_details', 'quantity']

    def get_product_details(self, obj):
        product = Product.objects.filter(id=obj.product.id).first()
        return ProductSerilaizer(product).data

    # def get(self, obj):
    #  product =obj.product.all()
    #  print(product)
    #  return ProductSerilaizer(product, many=True).data
    
    # def get(self, obj):
    #    if self.context.get('request').method == 'GET':
    #     product = Product.objects.get(id=obj.product.id)
    #     print(product)
    #         # return product.id
    #    return ProductSerilaizer(product, many=True).data
    


    def validate(self, data):
     request = self.context.get('request')
     method = self.context.get('method')
     
     if method == 'POST':
        product = data.get('product')
        if not product:
            raise serializers.ValidationError("Product not found")
        product_obj = Product.objects.filter(id=product.id).first()
        if not product_obj:
            raise serializers.ValidationError("Product does not exist")
        data['product'] = product_obj
        cart = self.context.get('cart')
        if CartItem.objects.filter(product=product, cart=cart).exists():            
            raise serializers.ValidationError("Product is already in the cart")
        
     elif method == 'PUT':
            quantity=data.get('quantity')
            if not quantity:
                raise serializers.ValidationError("Quantity is required")
            if quantity < 1:
                raise serializers.ValidationError("Quantity must be greater than 0")
     return data

    def update(self, instance, validated_data):
       instance.quantity = validated_data.get('quantity', instance.quantity)
       instance.save()
       return instance

    def create(self,validated_data):
        return CartItem.objects.create(**validated_data);
     
class CartSerializer(serializers.Serializer):
    # id=serializers.IntegerField();
    user=serializers.PrimaryKeyRelatedField(read_only=True);
    cart_items=CartItemSerializer(many=True);

    
    def get_cart_items(self, obj):
        cart_items = obj.cart_items.all()
        return CartItemSerializer(cart_items, many=True).data
    