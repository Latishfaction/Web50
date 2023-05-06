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
    path("<int:id>/placebid", views.place_bid, name="place_bid"),
    path("create", views.create_listing, name="create_listing"),
    path("mylistings", views.show_listings, name="show_listing"),
    path("mylistings/<int:id>", views.view_listing, name="view_listing"),
    path("mylistings/add", views.add_listing, name="add_listing"),
    path("My Watchlist/", views.show_watchlist, name="show_watchlist"),
    path("add/<int:listing_id>", views.addtoWatchlists, name="add_to_watchlist"),
    path(
        "remove/<int:listing_id>",
        views.removeWatchlist_item,
        name="remove_watchlist_item",
    ),
    path(
        "categories",
        views.show_categories,
        name="show_categories",
    ),
    path(
        "categories/<int:category_id>",
        views.show_category_listing,
        name="show_category_listing",
    ),
    path(
        "<int:listing_id>/publish_comment",
        views.post_comments,
        name="post_comments",
    ),
    path(
        "<int:listing_id>",
        views.show_comments,
        name="show_comments",
    ),
]
