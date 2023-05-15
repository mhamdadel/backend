from ecommerce.models import Product
from authentication.models import CustomUser
from django.db import models

class Cart(models.Model):
    # user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='cart',
    )
    
class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart_items")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_items")
    quantity=models.IntegerField(default=1)

    

