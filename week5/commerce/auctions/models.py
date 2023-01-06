from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# Auctions lists
class listings(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=300)
    price = models.IntegerField()
    url = models.URLField(max_length=400)
    category = models.CharField(max_length=20)