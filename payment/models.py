from django.db import models
from orders.models import Order

# Create your models here.
class Payment(models.Model):
    payment_id = models.BigAutoField(primary_key=True)
    oid = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='orders_payment')
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method_choices=[
        ("online","online"),
        ('offline', 'offline'),
    ]
    payment_method = models.CharField(max_length=50,choices= payment_method_choices ,default='online')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    isPaid = models.BooleanField
    shipping_Price = models.IntegerField(default=50)

    def get_total_amount(self):
        return (self.amount - self.shipping_Price)
    