from django.contrib import admin

from .models import Listing, Bid, ListingComment

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner_id', 'initial_price', 'end_at', 'is_active', 'winner_id')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'owner_id__username')
    ordering = ('-created_at',)

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('listing_id', 'user_id', 'amount')
    list_filter = ('listing_id', 'user_id')
    search_fields = ('listing_id__name', 'user_id__username')
    ordering = ('-amount',)

@admin.register(ListingComment)
class ListingCommentAdmin(admin.ModelAdmin):
    list_display = ('listing_id', 'user_id', 'content')
    list_filter = ('listing_id', 'user_id')
    search_fields = ('listing_id__name', 'user_id__username')
    ordering = ('-created_at',)