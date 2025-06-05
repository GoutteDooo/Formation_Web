from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import User, Post, FollowModel
from .forms import PostForm


def index(request):
    form = PostForm()
    return render(request, "network/index.html", { "form":form })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
@require_POST
def new_post(request):
    form = PostForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data["content"]
        print(form.cleaned_data)
        # create post object
        # add all necessary datas
        post = Post(
            user = request.user,
            content = content,
        )
        # save it to db
        post.save()

        return JsonResponse({
            "message":"Post sent successfully!",
            "content":content
        })
    else:
        return JsonResponse({"message": "Invalid form", "details": form.errors}, status=400)

def load_posts(request, posts_type):
    if posts_type == "all":
        posts = Post.objects.all()

    elif posts_type == "following":
        posts = Post.objects.none()  # à implémenter plus tard

    elif posts_type.startswith("profile-"):
        try:
            poster_id = int(posts_type.split("-")[1])
        except (IndexError, ValueError):
            return JsonResponse({"error": "Invalid profile ID"}, status=400)

        poster = User.objects.filter(id=poster_id).first()
        if not poster:
            return JsonResponse({"error": "User not found"}, status=404)

        posts = Post.objects.filter(user=poster)

    else:
        return JsonResponse({"error": "Invalid posts_type."}, status=400)

    posts = posts.order_by("-timestamp")
    return JsonResponse([post.serialize() for post in posts], safe=False)



@login_required
def profile_view(request, profile_id):
    """send required datas as follows as a JSON Object:
        - number of followers (int)
        - number of following (int)
        - following button (bool)
    """
    profile = User.objects.get(pk=profile_id)
    if request.user.is_authenticated:
        if profile_id != request.user.id:
            #check if profile is already follows
            following_button = FollowModel.objects.filter(follower = request.user.id, following = profile_id).exists()
            return JsonResponse({
                    "profile_id":profile.id,
                    "profile_name":profile.username,
                    "following_button":following_button,
                    "followers_count": profile.followers.count(),
                    "following_count": profile.following.count()
                })
        else: 
            #this is the user profile
            return JsonResponse({
                "profile_id":profile.id,
                "profile_name":profile.username,
                "followers_count": profile.followers.count(),
                "following_count": profile.following.count()
        })
    return JsonResponse({"error": "Not authenticated"}, status=403)