from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User,Bid,Listing,Category,Watchlist


def index(request):
    activeListing = Listing.objects.all().filter(isActive=True)
    return render(request, "auctions/index.html",{
        "activeItems":activeListing,
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

def auction_listing_view(request,id):
    listing = Listing.objects.get(pk=id)
    bid_info = list(Bid.objects.all().filter(item= listing))
    if len(bid_info)<=0:
        bid_info = None
    else:
        bid_info = bid_info[-1]
    return render(request,"auctions/list_view.html",{
        "list":listing,
        "owner": listing.owner.username == request.user.username,
        "bid_info" : bid_info,
        }
    )

def disable_bid(request,id):
    listing = Listing.objects.get(pk=id)
    listing.isActive = False
    listing.save()
    return HttpResponseRedirect(reverse('auction_listing_view',args=(listing.id,)))

def enable_bid(request,id):
    listing = Listing.objects.get(pk=id)
    # make bid on that item
    new_bid =Bid()
    new_bid.bidder = User.objects.get(username=request.user.username)
    new_bid.item = listing
    new_bid.bid_amount = listing.price
    new_bid.save()
    # change listing to active
    listing.isActive = True
    listing.save()
    return HttpResponseRedirect(reverse('auction_listing_view',args=(listing.id,)))


@login_required(login_url="login")
def place_bid(request,id,bidinfo):
    listing = AuctionListing.objects.get(pk=id)
    if request.method=="POST":
    # check if bid_amount > current bid price
        bid_amount = request.POST["bid_amount"]
        bid_amount = int(bid_amount)
        if bid_amount > bidinfo:
            # setting up new bid
            bid = Bid()
            bid.bidder = User.objects.get(username=request.user.username)
            bid.item = listing
            bid.bid_amount = bid_amount
            # saving item price as old bid
            bid.old_bid = listing.item.price
            bid.save()
            # changing the auction price as bid
            listing.price = bid_amount
            listing.save()
            messages.success(request, 'Bid is placed successfully! ')
            return HttpResponseRedirect(reverse("auction_listing",args=(id,)))

        else:
            messages.error(request, 'Bid must be greater than current bid')
            return HttpResponseRedirect(reverse("auction_listing",args=(id,)))

@login_required(login_url="login")
def show_listings(request):
    current_user = User.objects.get(username=request.user.username)
    return render(request,"auctions/listings.html",{
        "listings" : Listing.objects.all().filter(owner=current_user),
    })
@login_required(login_url="login")
def view_listing(request,id):
    return render(request,"auctions/list_view.html",{
        "list" : Listing.objects.get(pk=id),
        "owner": listing.owner.username == request.user.username,
    })

@login_required(login_url="login")
def create_listing(request):
    categories = Category.objects.all()
    return render(request,"auctions/createlisting.html",{
        "categories" : categories,
    })
@login_required(login_url="login")
def add_listing(request):
    if request.method =="POST":
        # fetch deatils of listing
        new_listing = Listing()
        new_listing.owner = User.objects.get(username=request.user.username)
        new_listing.title  = request.POST["title"]
        new_listing.description = request.POST["description"]
        new_listing.price = int(request.POST["price"])
        new_listing.theme = Category.objects.get(pk=int(request.POST["category"]))
        
        if len(request.POST['url']) !=0 :
            new_listing.url = request.POST["url"]
        
        
        new_listing.save()
        return HttpResponseRedirect(reverse("show_listing"))



def show_watchlist(request):
    user = User.objects.get(username=request.user.username)
    try:
        watchlist = Watchlist.objects.get(user=user)
        watchlist = watchlist.items.all()
    except(Exception):
        watchlist = []
    return render(request, "auctions/listings.html",{
        "listings":watchlist,
    })