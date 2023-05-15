from ecommerce.models import Product
from authentication.models import CustomUser
from django.db import models

class Wishlist(models.Model):
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name='wishlist')
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)