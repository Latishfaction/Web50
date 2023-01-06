from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# Auction Categories
class Category(models.Model):
    category = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.id} : {self.category}"

# Auctions lists
class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=500)
    price = models.PositiveIntegerField()
    url = models.URLField(max_length=400)
    theme = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="theme")

    def __str__(self):
        return f"{self.id} : {self.title} | {self.owner}"
