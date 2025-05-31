from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("update_watchlist/<int:listing_id>", views.update_watchlist, name="update_watchlist"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("close_listing/<int:listing_id>", views.close_listing, name="close_listing"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)