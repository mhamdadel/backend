from ecommerce.models import Product
from authentication.models import CustomUser
from django.db import models

class Cart(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)


class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="items")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="cart_items")
    quantity=models.IntegerField(default=1)

    

