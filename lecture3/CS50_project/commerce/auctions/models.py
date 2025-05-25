from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    name = models.CharField(max_length=64)
    description = models.TextField()
    picture_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField()
    bids_count = models.IntegerField(default=0)
    last_bid_id = models.ForeignKey("Bid", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name}: ${self.last_bid_id.amount} - end at: {self.end_at}"

class Bid(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user_id} bid ${self.amount} on {self.listing_id}"

class ListingComment(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} commented on {self.listing_id}: {self.content}"
        