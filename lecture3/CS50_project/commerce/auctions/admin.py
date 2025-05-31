from django.contrib import admin
from django.utils.html import format_html

from .models import Listing, Bid

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('name', 'initial_price', 'end_at', 'is_active')

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'listing', 'user', 'created_at')
    
    def created_at(self, obj):
        return obj.created_at
    created_at.admin_order_field = 'created_at'
    created_at.short_description = 'Created At'

    def listing(self, obj):
        return obj.listing_id.name if obj.listing_id else 'N/A'
    listing.short_description = 'Listing'

    def user(self, obj):
        return obj.user_id.username if obj.user_id else 'N/A'
    user.short_description = 'User'
