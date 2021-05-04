from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"), # Use listing id
    path("close_listing/<int:listing_id>", views.close_listing, name="close_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_to_watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:listing_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("place_bid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("categories", views.categories, name="categories"),

    # API ROUTES
]
