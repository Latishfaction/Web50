from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:id>", views.auction_listings, name="auction_listing"),
    path("<int:id> <int:bidinfo>/bid", views.place_bid, name="place_bid"),
]
