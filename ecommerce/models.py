from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    image = CloudinaryField("image", default="https://res.cloudinary.com/deg0m2eu4/image/upload/v1683417294/samples/food/spices.jpg")
    REQUIRED_FIELDS = ['name']
    class Meta:
        ordering = ['name']


    @property
    def image_url(self):
        return (
            f"https://res.cloudinary.com/dpoix2ilz/{self.image}"
        )
    
    def __str__(self):
        return self.name


class Product(models.Model):
    title= models.CharField(max_length=256)
    price= models.FloatField()
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description= models.TextField()
    Image = CloudinaryField("image")
    inStock= models.IntegerField()
   
    @property
    def image_url(self):
        return (
            f"https://res.cloudinary.com/dpoix2ilz/{self.image}"
        )
    
    REQUIRED_FIELDS = ['title', 'price', 'description', 'Image', 'inStock']


    def __str__(self):
        return self.title
