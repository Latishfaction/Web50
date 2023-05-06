from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from .models import User, Bid, Listing, Category, Watchlist, Comment


def index(request):
    activeListing = Listing.objects.all().filter(isActive=True)
    try:
        end_auction_item = Bid.objects.filter(isFinished=True)
    except:
        end_auction_item = []
    print(end_auction_item)
    return render(
        request,
        "auctions/index.html",
        {
            "activeItems": activeListing,
            "end_auction_item": reversed(end_auction_item),
        },
    )


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="login")
def auction_listing_view(request, id):
    listing = Listing.objects.get(pk=id)
    user = User.objects.get(username=request.user.username)
    bid_info = list(Bid.objects.all().filter(item=listing))
    watchlist_status = False
    if len(bid_info) <= 0:
        bid_info = None
    else:
        bid_info = bid_info[-1]
    try:
        item_watchlist = user.watcher.filter().last().items.all()
        for z in item_watchlist:
            if z.item == listing:
                watchlist_status = True
    except:
        item_watchlist = []
    # print(item_watchlist)
    # print(watchlist_status)
    return render(
        request,
        "auctions/list_view.html",
        {
            "list": listing,
            "owner": listing.owner.username == request.user.username,
            "bid_info": bid_info,
            "Iswatchlist": watchlist_status,
            "comments": show_comments(request, listing.id),
        },
    )


def disable_bid(request, id):
    listing = Listing.objects.get(pk=id)
    # get bid
    bid = Bid.objects.filter(item=listing).last()
    # check if bid has check
    # if no change then delete the bid
    if listing.price == bid.bid_amount:
        bid.delete()
    # if change in bid then show highest bidder details
    bid.isFinished = True
    bid.save()
    listing.isActive = False
    listing.save()
    return HttpResponseRedirect(reverse("auction_listing_view", args=(listing.id,)))


def enable_bid(request, id):
    listing = Listing.objects.get(pk=id)

    try:
        new_bid = listing.bid_item.last()
        new_bid.save()
    except:
        # make bid on that item
        new_bid = Bid()
        new_bid.bidder = User.objects.get(username=request.user.username)
        new_bid.item = listing
        new_bid.bid_amount = listing.price
        new_bid.save()
    # change listing to active
    listing.isActive = True
    listing.save()
    return HttpResponseRedirect(reverse("auction_listing_view", args=(listing.id,)))


@login_required(login_url="login")
def place_bid(request, id):
    listing = Listing.objects.get(pk=id)
    if request.method == "POST":
        # check if bid_amount > current bid price
        bid_amount = request.POST["bid_amount"]
        bid_amount = int(bid_amount)
        if bid_amount > listing.price:
            # setting up new bid
            bid = Bid()
            bid.bidder = User.objects.get(username=request.user.username)
            bid.item = listing
            bid.bid_amount = bid_amount
            bid.bid_starting_amt = listing.price
            # saving item price as old bid
            bid.save()
            # changing the auction price as bid
            listing.price = bid_amount
            listing.save()
            messages.success(request, "Bid is placed successfully! ")
            return HttpResponseRedirect(reverse("auction_listing_view", args=(id,)))

        else:
            messages.error(request, "Your Bid must be greater than current bid")
            return HttpResponseRedirect(reverse("auction_listing_view", args=(id,)))


@login_required(login_url="login")
def show_listings(request):
    current_user = User.objects.get(username=request.user.username)
    return render(
        request,
        "auctions/listings.html",
        {
            "listings": Listing.objects.all().filter(owner=current_user),
        },
    )


@login_required(login_url="login")
def view_listing(request, id):
    return render(
        request,
        "auctions/list_view.html",
        {
            "list": Listing.objects.get(pk=id),
            "owner": listing.owner.username == request.user.username,
        },
    )


@login_required(login_url="login")
def create_listing(request):
    categories = Category.objects.all()
    return render(
        request,
        "auctions/createlisting.html",
        {
            "categories": categories,
        },
    )


@login_required(login_url="login")
def add_listing(request):
    if request.method == "POST":
        # fetch deatils of listing
        new_listing = Listing()
        new_listing.owner = User.objects.get(username=request.user.username)
        new_listing.title = request.POST["title"]
        new_listing.description = request.POST["description"]
        new_listing.price = int(request.POST["price"])
        new_listing.theme = Category.objects.get(pk=int(request.POST["category"]))

        if len(request.POST["url"]) != 0:
            new_listing.url = request.POST["url"]

        new_listing.save()
        return HttpResponseRedirect(reverse("show_listing"))


def show_watchlist(request):
    user = User.objects.get(username=request.user.username)
    watchlistItems = []
    try:
        watchlist = Watchlist.objects.get(user=user)
        watchlist = watchlist.items.all()
        for items in watchlist:
            watchlistItems.append(items.item)
    except Exception:
        watchlistItems = []
    return render(
        request,
        "auctions/listings.html",
        {
            "listings": watchlistItems[::-1],
        },
    )


def addtoWatchlists(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    bidding = list(Bid.objects.filter(item=listing))
    # get latest bid to add into watchlist
    bid_latest = [bidding[-1]]
    # print(bid_latest)
    # get the current user
    current_user = User.objects.get(username=request.user.username)

    # find the watchlist item on existing watchlists
    try:
        #  pick the existing item on watchlists by user
        new_watchlist_item = Watchlist.objects.filter(user=current_user).last()
    except:
        # otherwise create new user entry
        new_watchlist_item = Watchlist.objects.create(user=current_user)
    for bids in bid_latest:
        new_watchlist_item.items.add(bids)
    new_watchlist_item.save()
    return HttpResponseRedirect(reverse("auction_listing_view", args=(listing_id,)))


def removeWatchlist_item(request, listing_id):
    # get the item from listing_id
    listing = Listing.objects.get(id=listing_id)
    bidding = list(Bid.objects.filter(item=listing))
    # find the watchlists item
    new_watchlist_item = Watchlist.objects.filter(
        user=User.objects.get(username=request.user.username)
    ).last()
    # remove the specified item
    bid_latest = [bidding[-1]]
    for bids in bid_latest:
        new_watchlist_item.items.remove(bids)

    new_watchlist_item.save()
    return HttpResponseRedirect(reverse("auction_listing_view", args=(listing_id,)))


def show_categories(request):
    category_list = Category.objects.filter()
    return render(
        request,
        "auctions/categories.html",
        {
            "categories": category_list,
        },
    )


def show_category_listing(request, category_id):
    listing = []
    category = Category.objects.get(id=category_id)
    category = category.theme.all()
    for items in category:
        if items.isActive == False:
            continue
        else:
            listing.append(items)
    return render(
        request,
        "auctions/listings.html",
        {
            "listings": listing,
            "err_msg": f"No Active listing on {category.first().theme.category}",
        },
    )


# save comments
def post_comments(request, listing_id):
    if request.method == "POST":
        # get item from listing_id
        listing = Listing.objects.get(id=listing_id)
        # get user
        user = User.objects.get(username=request.user.username)
        # get comment from form textarea
        comment = request.POST["comment"]

        # add values to the comment model
        comment_entry = Comment()
        comment_entry.user = user
        comment_entry.comment = comment
        comment_entry.listing = listing
        comment_entry.created_at = datetime.now()

        # save model
        comment_entry.save()

        return HttpResponseRedirect(reverse("auction_listing_view", args=(listing.id,)))


def show_comments(request, listing_id):
    try:
        item = Listing.objects.get(id=listing_id)
        item = Bid.objects.filter(item=item).last().item
        item = item.item_comments.filter()
    except:
        item = []
    return reversed(item)
