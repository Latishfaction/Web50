from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# Auction Categories
class Category(models.Model):
    category = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.id} : {self.category}"


# Total Auctions lists
class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    price = models.IntegerField()
    url = models.URLField(
        max_length=400,
        default="https://us.123rf.com/450wm/pavelstasevich/pavelstasevich1811/pavelstasevich181101027/pavelstasevich181101027.jpg",
    )
    theme = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="theme")
    isActive = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} : {self.title} | {self.owner}"


# comments
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentor")
    # auto_now_add for adding time and date of comment
    # auto_now for updating time and date of comment (edit comment)
    created_at = models.DateTimeField(auto_now_add=False, auto_now=False)
    comment = models.TextField(max_length=500)
    # tells about commented on which listing
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="item_comments"
    )

    def __str__(self):
        return f"{self.user} : {self.listing.title} from {self.listing.theme.category} "


# Active Listing
class Bid(models.Model):
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bidder", null=True
    )
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_item")
    bid_amount = models.PositiveIntegerField(default=0)
    bid_starting_amt = models.PositiveIntegerField(default=0)
    isFinished = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.id} : {self.bid_amount} | {self.bidder} | {self.item.title}"


# Watch list
class Watchlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="watcher", null=True
    )
    items = models.ManyToManyField(Bid, blank=True, related_name="watching")

    def __str__(self):
        return f"{self.user} has {len(self.items.all())} items"
