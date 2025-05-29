from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import User, Listing


def index(request):
    return render(request, "auctions/index.html")


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    default_end = timezone.now() + timezone.timedelta(days=7)
    if request.method == "POST":
        listing = {
            "name": request.POST["name"],
            "description": request.POST["description"],
            "initial_price": request.POST["initial_price"],
            "picture_url": request.POST["picture_url"],
            "end_at": request.POST["end_at"],
            "category": request.POST["category"],
            "owner_id": request.user
        }
        for key, value in listing.items():
            if not value and key != "picture_url":
                return render(request, "auctions/createListing.html", {
                    "message": f"Please fill {key} field",
                    "default_end": default_end.strftime("%Y-%m-%d")
                })
        listing = Listing.objects.create(**listing)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/createListing.html", {
            "default_end": default_end.strftime("%Y-%m-%d")
        })