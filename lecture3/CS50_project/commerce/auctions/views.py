from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


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
        # Get form data
        name = request.POST.get("name")
        description = request.POST.get("description")
        initial_price = request.POST.get("initial_price")
        picture = request.FILES.get("picture_url")
        end_at = request.POST.get("end_at")
        category = request.POST.get("category")
        
        # Validate required fields
        if not all([name, description, initial_price, end_at]):
            return render(request, "auctions/createListing.html", {
                "message": "Please fill all required fields",
                "default_end": default_end.strftime("%Y-%m-%d")
            })

        # Create listing
        listing = Listing(
            owner_id=request.user,
            name=name,
            description=description,
            initial_price=initial_price,
            picture_url=picture,
            end_at=end_at,
            category=category
        )
        
        # Save the listing and handle the image upload
        try:
            listing.save()
            if picture:
                listing.picture_url.save(picture.name, picture, save=True)
            return HttpResponseRedirect(reverse("index"))
        except Exception as e:
            return render(request, "auctions/createListing.html", {
                "message": f"Error saving listing: {str(e)}",
                "default_end": default_end.strftime("%Y-%m-%d")
            })
    else:
        return render(request, "auctions/createListing.html", {
            "default_end": default_end.strftime("%Y-%m-%d")
        })

def listing(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        return render(request, "auctions/listing.html", {
            "listing_error": "Listing not found"
        })
    return render(request, "auctions/listing.html", {
        "listing": listing
    })

@login_required
def update_watchlist(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        return render(request, "auctions/listing.html", {
            "listing_error": "Listing not found"
        })
    if listing in request.user.watchlist.all():
        request.user.watchlist.remove(listing)
    else:
        request.user.watchlist.add(listing)
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))
        

@login_required
def bid(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        return render(request, "auctions/listing.html", {
            "listing_error": "Listing not found"
        })
    if request.method == "POST":
        amount = float(request.POST.get("amount"))
        if listing.last_bid_id and amount <= listing.last_bid_id.amount:
            return render(request, "auctions/listing.html", {
                "error": "Bid must be higher than last bid",
                "listing": listing
            })
        elif amount <= listing.initial_price:
            return render(request, "auctions/listing.html", {
                "error": "Bid must be higher than initial price",
                "listing": listing
            })
        bid = Bid(
            listing_id=listing,
            user_id=request.user,
            amount=amount
        )
        bid.save()
        listing.last_bid_id = bid
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
