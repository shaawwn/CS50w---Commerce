from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Bid, Comment, Category, WatchList
from .forms import ListingForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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
    user = User.objects.get(username=request.user)
    watchlist = WatchList.objects.filter(watching=user)
    watching = False

    for item in watchlist:
        if item.listing == listing:
            watching = True


    for bid in bids:
        if bid.bid == max([bid.bid for bid in bids]):
            max_bid = bid
    comments = Comment.objects.filter(listing=listing)

    if listing.open == False:
        messages.info(request, "You won the auction!")

    return render(request, 'auctions/listing.html', {
        "listing": listing,
        "bid": max_bid,
        "comments": comments,
        "watching": watching
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

@login_required(login_url='login')
def watchlist(request):

    # Get all the listings that a user is watching
    user = User.objects.get(username=request.user)
    watchlist = WatchList.objects.filter(watching=user)
    return render(request, 'auctions/watchlist.html', {
        "watchlist": watchlist
    })

def add_to_watchlist(request, listing_id):
    """Add a listing to current user's watchlist"""

    if request.method == 'POST':
        listing = Listing.objects.get(id=listing_id)
        user = User.objects.get(username=request.user)
        to_watch = WatchList(listing=listing)
        try:
            to_watch = WatchList.objects.get(listing=listing)
        except:
            to_watch = WatchList(listing=listing)
            to_watch.save()

        to_watch.watching.add(user)
        to_watch.save()

    return HttpResponseRedirect(reverse('listing', args=[listing_id]))


def remove_from_watchlist(request, listing_id):
    """Allow users to remove an item from their watchlist"""
    if request.method == 'POST':
        listing = Listing.objects.get(id=listing_id)
        user = User.objects.get(username=request.user)
        to_unwatch = WatchList.objects.get(listing=listing)

        to_unwatch.watching.remove(user)
        to_unwatch.save()

    return HttpResponseRedirect(reverse('listing', args=[listing_id]))

    


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