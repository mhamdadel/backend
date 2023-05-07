from orders.models import OrderItem
from orders.models import Order
from rest_framework import serializers



class Order_ItemSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField(read_only=True)
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    image= serializers.ImageField()
    class Meta:
        model = OrderItem
        fields = ['cart_id', 'quantity', 'price', 'image']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for order_item_data in order_items_data:
            OrderItem.objects.create(order=order, **order_item_data)
        return order
    
    
class OrderSerializer(serializers.Serializer):
    order_items = Order_ItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['order_id', 'uid', 'createdAt', 'cancellation_deadline',   'shipping_address', 'cancellation_fees', 'phone_number', 'status', 'order_items']
    order_id = serializers.IntegerField(read_only=True)
    uid = serializers.IntegerField(read_only=True)
    createdAt = serializers.DateTimeField()
    cancellation_deadline = serializers.DateTimeField()
    shipping_address = serializers.CharField()
    phone_number = serializers.CharField()
    status = serializers.CharField()


