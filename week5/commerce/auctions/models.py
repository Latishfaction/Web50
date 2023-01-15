from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# Auction Categories
class Category(models.Model):
    category = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.id} : {self.category}"


# Auctions lists
class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=500)
    price = models.IntegerField()
    url = models.URLField(max_length=400)
    theme = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="theme")

    def __str__(self):
        return f"{self.id} : {self.title} | {self.owner}"


#comments
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="commentor")
    # auto_now_add for adding time and date of comment
    # auto_now for updating time and date of comment (edit comment)
    created_at = models.DateTimeField(auto_now_add=True,auto_now=False)
    comment = models.TextField(max_length=500)
    # tells about commented on which listing
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,related_name="comments")

    def __str__(self):
        return f"{self.user} : {self.listing.title} from {self.listing.theme.category} "

#live auctions
class AuctionListing(models.Model):
    isActive = models.BooleanField(default=False)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE,related_name="active_items",null=True)

    def __str__(self):
        return f"{self.id} : {self.item.title}"

# bid
class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE,related_name="bidder",null=True)
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE,related_name="bid_item")
    bid_amount = models.PositiveIntegerField()
    old_bid = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.id} : {self.bid_amount} | {self.bidder} | {self.item.item.title}"


# Watch list
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user",null=True)
    items = models.ManyToManyField(Listing)

    def __str__(self):
        return f"{self.user} has {len(self.items.all())} items"