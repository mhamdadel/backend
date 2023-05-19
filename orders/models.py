from ecommerce.models import Product
from django.db import models
from authentication.models import CustomUser
from django.core.validators import RegexValidator
from django.utils import timezone

class Order(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    uid = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='orders')
    createdAt = models.DateTimeField(auto_now_add=True)
    cancellation_deadline = models.DateTimeField(null=True, default=None)   
    shipping_address = models.TextField()
    # billing_address = models.TextField(null=True)
    cancellation_fees=models.IntegerField(default=0)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(('phone number'), validators=[phone_regex], max_length=17, blank=True)    
    status_choices=[
        ("pending","pending"),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled','Cancelled')
    ]
    status = models.CharField(max_length=20,choices= status_choices, default='PENDING')

    
    def get_cancellation_fees(self):
        cancellation_fees = 0
        order_date = self.createdAt
        current_date = timezone.now()
        days_difference = (current_date - order_date).days
        print(days_difference)
        if days_difference > 2:
            cancellation_fees = 500
        return cancellation_fees
    
    def get_total_amount(self):
        order_items = self.order_items.all()
        if(order_items.exists()):
          total=sum(item.get_total() for item in order_items)
          return total-self.get_cancellation_fees()
        else:return 0
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="products",default=6)
    # product=models.OneToOneField(Product, on_delete=models.CASCADE, related_name='product')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def get_total(self):
        return self.quantity * self.price 
    