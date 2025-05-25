from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    picture_url = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bids_count = models.IntegerField(default=0)
    last_bid_id = models.ForeignKey("Bid", on_delete=models.SET_NULL, null=True)
