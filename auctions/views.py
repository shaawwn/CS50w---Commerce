from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Bid, Comment, Category
from .forms import ListingForm

# ----------------------------- MAIN PAGE --------
def index(request):

    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
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

# ------------ PAGES

def add_listing(request):
    print("REQUEST:", request.POST)
    if request.method == 'POST':
        form = ListingForm(request.POST)
        # Save as a model

        category = Category.objects.filter(cat_type=request.POST['category'])
        if len(category) == 0:
            category = Category(cat_type=request.POST['category'])
            category.save()
            category = Category.objects.filter(cat_type=request.POST['category'])
        # listing = Listing.objects.create(title=request.POST['title'], description=request.POST['description'], starting_bid=request.POST['starting_bid'], category=request.POST['category'])
        listing = Listing(title=request.POST['title'], description=request.POST['description'], starting_bid=request.POST['starting_bid'], seller=request.user)
        listing.save()
        bid = Bid(listing=listing, bid=listing.starting_bid)
        bid.save()
        listing.category.set(category)
        return HttpResponseRedirect(reverse('listing', args=[listing.id]))
        # return render(request, f'auctions/listing/{int(listing.id)}')
    form = ListingForm()
    return render(request, 'auctions/add_listing.html', {
        "form": form
    })


def listing(request, listing_id):

    listing = Listing.objects.get(id=listing_id)
    bids = Bid.objects.filter(listing=listing)

    print(max(bids).bid)
    comments = Comment.objects.filter(listing=listing)
    return render(request, 'auctions/listing.html', {
        "listing": listing,
        "bids": max(bids),
        "comments": comments
    })


def watchlist(request):
    
    return render(request, 'auctions/watchlist.html')


def categories(request):

    return render(request, 'auctions/categories.html')