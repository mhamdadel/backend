from django.db import models
from authentication.models import CustomUser
from django.core.validators import RegexValidator

# Create your models here.

class Order(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    uid = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='orders'),
    createdAt = models.DateTimeField(auto_now_add=True)
    cancellation_deadline = models.DateTimeField()
    shipping_address = models.TextField()
    billing_address = models.TextField()
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
    def get_total_amount(self):
        order_items = self.order_items.all()
        return sum(item.get_total() for item in order_items) if order_items.exists() else 0
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def get_total(self):
        return self.quantity * self.price 
    