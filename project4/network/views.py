from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, FollowModel, PostLikes
from .forms import PostForm
import json


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
        # displays all posts from the user's following
        # get the list of all user's following
        following_users = FollowModel.objects.filter(
            follower = request.user
        ).values_list("following", flat=True)
        print("following_list:",following_users)
        posts = Post.objects.filter(
            user__in = following_users
        )
        print("posts:",posts)

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

    post_list = posts.order_by("-timestamp")

    #Get page number from query params (?page=2)
    page_number = request.GET.get("page",1)

    #Paginator with 10 posts per page
    paginator = Paginator(post_list, 10)

    #Get the specific page
    page_obj = paginator.get_page(page_number)


    return JsonResponse(
        {
            "posts": [post.serialize() for post in page_obj],
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "num_pages": paginator.num_pages,
            "current_page": page_obj.number
        }
        , safe=False)



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
            print("following_button:",following_button)
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

@require_POST
@login_required
def follow(request, profile_id):
    """
    If the profile_id is followed by user, this function will insert 
    into the FollowModel table a new row which is :
        Follower : user.id
        Following : profile_id
    
    If the profile_id is unfollowed, this function will remove from
    FollowModel the row concerned.

    Then, it will send back a JsonResponse and JS will handle it back.
    """
    # see if user is already following profile
    is_follow = FollowModel.objects.filter(
        follower = request.user,
        following = profile_id
    ).exists()
    if is_follow:
        # if it is, remove the row
        FollowModel.objects.get(
            follower = request.user,
            following = profile_id
        ).delete()
        return JsonResponse({
            "message":f"You removed {profile_id} from your followings.",
            "toggle":True
        })
    else:
        # else, add a new row
        profile_user = User.objects.get(pk=profile_id)
        new_followModel = FollowModel(
            follower = request.user,
            following = profile_user
        )
        new_followModel.save()
        return JsonResponse({
            "message":f"You follow {profile_id}!",
            "toggle":False
        })
    return JsonResponse({
        "error":"Server error."
    }, status=500)

@csrf_exempt
@login_required
def edit_post(request, post_id):
    if request.method != "PATCH":
        return JsonResponse({"error":"PATCH request desired"}, status=405)

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExit:
        return JsonResponse({"error":"Post not found"}, status=404)

    #check if post is users one
    user_id = request.user.id
    user_post_id = post.user_id
    
    if user_id != user_post_id:
        return JsonResponse({"error":"User does not own this post"}, status=403)

    try:
        data = json.loads(request.body)
        registered_text = data.get("registeredText")

        if registered_text is not None:
            # edit content of post
            post.content = registered_text
            post.save()

            return JsonResponse({
                "message":"Post updated successfully!",
                "edited_text":post.content
                })

        else:
            return JsonResponse({"error":"RegisteredText is missing"}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({"error":"Invalid JSON"}, status=400)

def like_post(request, post_id):
    # check in the Like table and see if post is already liked
    like = Postlikes.objects.get(
        post = post_id,
        user = request.user
    )
    # if it is not the case, add a new row
    # and send appropriate response
    if like is None:
        post_like = PostLikes(
            user = request.user,
            post = post_id
        )
        post_like.save()

        return JsonResponse({
            "message":f"Post {post_id} liked",
            "is_liked":True
            })
    # else, post is already like, so remove the row
    # and send the appropriate response
    else:
        like.delete()
        return JsonResponse({
            "message":f"Post {post_id} unliked",
            "is_liked":False
            })
    return JsonResponse({"message":"server response"})