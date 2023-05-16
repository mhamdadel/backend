from authentication.models import CustomUser
from cart.models import Cart
from ecommerce.models import Product
from orders.models import OrderItem
from orders.models import Order
from rest_framework import serializers
from ecommerce.serializers import ProductSerilaizer


class Order_ItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    product = ProductSerilaizer(many=False, read_only=True)
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    # image= serializers.ImageField(max_length=None, use_url=True,required=False)
    class Meta:
        model = OrderItem
        fields = ['order','product', 'quantity', 'price']
        
    # def create_order_item(self, validated_data):
    #     order_item = OrderItem.objects.create(**validated_data)
    #     return order_item   
  


    
    
class OrderSerializer(serializers.ModelSerializer):
    order_items = Order_ItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [ 'order_id','uid', 'createdAt', 'cancellation_deadline',   'shipping_address', 'cancellation_fees', 'phone_number', 'status', 'order_items']
    order_id = serializers.StringRelatedField(read_only=True)
    uid = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    createdAt = serializers.DateTimeField()
    cancellation_deadline = serializers.DateTimeField()
    shipping_address = serializers.CharField()
    phone_number = serializers.CharField()
    status = serializers.CharField()

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for order_item_data in order_items_data:
            OrderItem.objects.create(order=order, **order_item_data)
        return order

    
    def get_order_items(self, obj):
        order_items = obj.order_items.all()
        return Order_ItemSerializer(order_items, many=True).data  