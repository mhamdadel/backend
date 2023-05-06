from rest_framework import serializers


class OrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(read_only=True)
    uid = serializers.IntegerField(read_only=True)
    createdAt = serializers.DateTimeField()
    cancellation_deadline = serializers.DateTimeField()
    shipping_address = serializers.CharField()
    billing_address = serializers.CharField()
    phone_number = serializers.CharField()
    status = serializers.CharField()