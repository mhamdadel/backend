from django.db import models

class Base (models.Model):
    name = models.CharField(max_length=255)

