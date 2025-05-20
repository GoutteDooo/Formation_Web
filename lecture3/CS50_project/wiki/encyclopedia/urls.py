from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("new/save/", views.save_new, name="save_new"),
    path("edit/", views.edit, name="edit"),
    path("edit/save/", views.save_edit, name="save_edit")
]
