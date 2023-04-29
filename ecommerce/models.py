from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    REQUIRED_FIELDS = ['name']
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name