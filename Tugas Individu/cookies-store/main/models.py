import uuid
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)