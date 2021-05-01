from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("listing", views.listing, name="listing"), # Use listing id
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),

    # API ROUTES
]
