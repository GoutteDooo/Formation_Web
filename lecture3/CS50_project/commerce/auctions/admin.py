from django.contrib import admin
from django.utils.html import format_html

from .models import Listing, Bid

admin.site.register(Listing)
admin.site.register(Bid)