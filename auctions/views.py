from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Bid, Comment, Category
from .forms import ListingForm
from django.contrib import messages


# ----------------------------- MAIN PAGE --------
def index(request):
    listings = Listing.objects.filter(open=True)
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
    print("REQUEST:", request.POST, request.FILES)
    if request.method == 'POST':
        form = ListingForm(request.POST)
        category = Category.objects.filter(cat_type=request.POST['category'])
        if len(category) == 0:
            category = Category(cat_type=request.POST['category'])
            category.save()
            category = Category.objects.filter(cat_type=request.POST['category'])
        # listing = Listing.objects.create(title=request.POST['title'], description=request.POST['description'], starting_bid=request.POST['starting_bid'], category=request.POST['category'])
        listing = Listing(title=request.POST['title'], description=request.POST['description'], starting_bid=request.POST['starting_bid'], image=request.FILES['image'], seller=request.user)
        listing.save()
        bid = Bid(listing=listing, bid=listing.starting_bid, bidder=request.user)
        bid.save()
        listing.category.set(category)
        return HttpResponseRedirect(reverse('listing', args=[listing.id]))
        # return render(request, f'auctions/listing/{int(listing.id)}')

    form = ListingForm()
    return render(request, 'auctions/add_listing.html', {
        "form": form
    })


def listing(request, listing_id):
    """Display listing item"""
    listing = Listing.objects.get(id=listing_id)
    bids = Bid.objects.filter(listing=listing)

    # print(bids)
    comments = Comment.objects.filter(listing=listing)
    return render(request, 'auctions/listing.html', {
        "listing": listing,
        "bid": max([bid.bid for bid in bids]),
        "bidder": Bid.objects.get(bid=max([bid.bid for bid in bids])),
        "comments": comments
    })


def close_listing(request, listing_id):
    """Allow a seller to close a listing"""
    # Listing should display who the winner is

    if request.method == 'POST':
        listing = Listing.objects.get(id=listing_id)
        # bid = Bid.objects.get(listing=listing)
        listing.open = False
        listing.save()

    return HttpResponseRedirect(reverse('listing', args=[listing_id]))


def watchlist(request):
    
    return render(request, 'auctions/watchlist.html')

def place_bid(request, listing_id):
    """Users may place a bid on an item"""

    user = User.objects.filter(username=request.user)
    if request.method == 'POST':
        listing = Listing.objects.get(id=listing_id)
        bids = Bid.objects.filter(listing=listing)
        max_bid = max([bid.bid for bid in bids])

        try:
            if float(request.POST['bid']) <= max_bid:
                messages.error(request, "Your bid must be higher than current bid")
                return HttpResponseRedirect(reverse('listing', args=[listing_id]))

        except ValueError:
            messages.error(request, "You must enter a bid")
            return HttpResponseRedirect(reverse('listing', args=[listing_id]))

        new_bid = Bid(listing=listing, bid=request.POST['bid'], bidder=request.user)

        new_bid.save()
        listing.top_bidder.set(user)
        listing.save()

    messages.info(request, "Bid placed sucessfully!")
    return HttpResponseRedirect(reverse('listing', args=[listing_id]))




def categories(request):

    return render(request, 'auctions/categories.html')