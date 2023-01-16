from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User,AuctionListing,Bid,Listing,Category


def index(request):
    lists = AuctionListing.objects.all()
    return render(request, "auctions/index.html",{
        "activeItems":lists,
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

def auction_listings(request,id):
    listing = AuctionListing.objects.get(pk=id)
    latest_bid = list(listing.bid_item.all())
    return render(request,"auctions/auction_listing.html",{
        "list":listing,
        "bidinfo":latest_bid[-1],
        }
    )

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
    return render(request,"auctions/view_listing.html",{
        "listing" : Listing.objects.get(pk=id),
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



