from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User,AuctionListing,Bid,Listing


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

# change  to Auction
# update the bid
# change the auction price


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
            bid.old_bid = listing.item.price
            bid.save()
            listing.price = bid_amount
            listing.save()
            messages.success(request, 'Bid is placed successfully! ')
            return HttpResponseRedirect(reverse("auction_listing",args=(id,)))

        else:
            messages.error(request, 'Bid must be greater than current bid')
            return HttpResponseRedirect(reverse("auction_listing",args=(id,)))

    # if bid error then show error message with alerts







    
# @login_required(login_url="login")
# def place_bid(request,id):
#     bid = Bid.objects.get(pk=id)
#     Message = True
#     if request.method=="POST":
#     # check if bid_amount > current bid price
#         new_amount = request.POST["bid_amount"]
#         new_amount = int(new_amount)
#         current_amount = bid.bid_amount
#         list = Bid.objects.get(pk=id)
#         if new_amount > current_amount:
#             Add new Bid with all the fields
#             new_bid = Bid()
#             new_bid.bidder = User.objects.get(username=request.user.username)
#             new_bid.item = list.item
#             new_bid.bid_amount = new_amount
#             new_bid.old_bid = current_amount
#             new_bid.save()
#             print("Bidder : ",new_bid.bidder)
#             print("Item : ",new_bid.item)
#             print("Updated Amount : ",new_bid.bid_amount)
#             print("Previous AMt: ",new_bid.old_bid)

#             return render(request,"auctions/auction_listing.html",{
#                 "list":list.item,
#                 "bid":list,
#                 "success":True,
#                 "error":False,

#             }) 
#         else:
#             return render(request,"auctions/auction_listing.html",{
#                 "list":list.item,
#                 "bid":list,
#                 "success":False,
#                 "error":True,

#             }) 