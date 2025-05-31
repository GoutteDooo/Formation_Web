from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    watchlist = models.ManyToManyField("Listing", blank=True, related_name="watchlisted_by")

    def __str__(self):
        return self.username

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    name = models.CharField(max_length=64)
    description = models.TextField()
    initial_price = models.DecimalField(default=0,max_digits=10, decimal_places=2)
    picture_url = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField()
    bids_count = models.IntegerField(default=0)
    category = models.CharField(default="others", max_length=64)
    last_bid_id = models.ForeignKey("Bid", on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    winner_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name}: ${self.initial_price} - end at: {self.end_at.strftime('%Y-%m-%d %H:%M:%S')}"

    def get_min_bid_amount(self):
        """Return the minimum bid amount (either last bid amount or initial price)"""
        return self.last_bid_id.amount if self.last_bid_id else self.initial_price

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"{self.id}: Bid ${self.amount} by {self.user_id.username} on {self.listing_id.name}"

class ListingComment(models.Model):
    id = models.AutoField(primary_key=True)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id.username}: {self.content}"