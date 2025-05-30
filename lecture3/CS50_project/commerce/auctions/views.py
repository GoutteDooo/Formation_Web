from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, ListingComment
from .functions import set_winner

def index(request):
    # Get all active listings
    active_listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": active_listings
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

def watchlist(request):
    watchlist = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

def categories(request):
    categories = Listing.objects.values_list("category", flat=True).distinct()
    print("categories:", categories)
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category):
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings
    })

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
        comments = ListingComment.objects.filter(listing_id=listing_id).order_by("-created_at")
    except Listing.DoesNotExist:
        return render(request, "auctions/listing.html", {
            "listing_error": "Listing not found"
        })
    if not listing.is_active:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "error": "This listing is closed"
        })
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments
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
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        

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
        last_bid_amount = listing.last_bid_id.amount if listing.last_bid_id else listing.initial_price

        amount = round(amount, 2)
        last_bid_amount = round(last_bid_amount, 2)

        print("amount:", format(amount, '.2f'))
        print("last_bid_amount:", format(last_bid_amount, '.2f'))
        print("amount == last_bid_amount:", format(amount, '.2f') == format(last_bid_amount, '.2f'))

        if listing.last_bid_id and format(amount, '.2f') <= format(last_bid_amount, '.2f'):
            return render(request, "auctions/listing.html", {
                "error": f"Bid must be higher than last bid (which is ${last_bid_amount})",
                "listing": listing
            })
        elif amount <= listing.initial_price:
            return render(request, "auctions/listing.html", {
                "error": f"Bid must be higher than initial price (which is ${listing.initial_price})",
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

@login_required
def close_listing(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        return render(request, "auctions/listing.html", {
            "listing_error": "Listing not found"
        })
    if request.method == "POST":
        listing.winner_id = set_winner(listing)
        if listing.winner_id:
            listing.is_active = False
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "error": "Nobody bid, please wait for one before closing !"
            })

@login_required
def comment(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        return render(request, "auctions/listing.html", {
            "listing_error": "Listing not found"
        })
    if request.method == "POST":
        content = request.POST.get("content")
        if not content:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "error": "Comment cannot be empty"
            })
        comment = ListingComment(
            listing_id=listing,
            user_id=request.user,
            content=content
        )
        comment.save()
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
