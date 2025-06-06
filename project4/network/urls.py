
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("load_posts/<str:posts_type>", views.load_posts, name="load_posts"),
    path("profile/<int:profile_id>", views.profile_view, name="profile"),
    path("follow/<int:profile_id>", views.follow, name="follow"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post")
]
