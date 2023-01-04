from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class User(AbstractUser):
    pass

# category
class category(models.Model):
    category = models.CharField(max_length=30) 

#storing bidding details
class bid(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="bidder")
    current_bid = models.IntegerField()
   
    def __str__(self):
        return f"{self.id} >> Current Bid : {self.current_bid}"



# listings
class listings(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="lister")
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=200)
    
    # to set when upload the listing
    bid_amount = models.ForeignKey(bid, on_delete=models.CASCADE,related_name="bid_range")

    picture = models.URLField(max_length=300)
    
    #category data
    category = models.ForeignKey(category, on_delete = models.CASCADE,related_name="categories")




#comments 
class comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="commentor")
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=False,blank=True)
    comment = models.TextField(max_length=100)
    
    # comment on which product
    title = models.ForeignKey(listings,on_delete=models.CASCADE,related_name="product")

#auction list
class auctionlist(models.Model):
    # auction by which user
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="owner")
    title = models.ForeignKey(listings, on_delete=models.CASCADE,related_name="auction_product")
    category = models.ForeignKey(category,on_delete=models.CASCADE,related_name="auction_category")
    isActive = models.BooleanField()
    #for highest bidder
    highest_bid = models.ForeignKey(bid, on_delete=models.CASCADE,related_name="highest_bidder")
    comments = models.ForeignKey(comments, on_delete=models.CASCADE,related_name="auction_commentors")
