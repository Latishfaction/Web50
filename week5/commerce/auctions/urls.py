from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:id>", views.auction_listing_view, name="auction_listing_view"),
    path("<int:id>/enable_bid", views.enable_bid, name="enable_bid"),
    path("<int:id>/disable_bid", views.disable_bid, name="disable_bid"),
    path("<int:id> <int:bidinfo>/bid", views.place_bid, name="place_bid"),
    path("create",views.create_listing,name="create_listing"),
    path("mylistings",views.show_listings,name="show_listing"),
    path("mylistings/<int:id>",views.view_listing,name="view_listing"),
    path("mylistings/add",views.add_listing,name="add_listing"),
]
