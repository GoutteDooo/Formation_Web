from django.contrib import admin

from .models import Listing, Bid, ListingComment

admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(ListingComment)