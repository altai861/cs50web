from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add, name="add"),
    path("view/<int:listing_id>", views.view_listing, name="view"),
    path("watchlist/add/<int:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("watchlist/remove/<int:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("close/<int:listing_id>", views.close_auction, name="close_auction"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("category_listings/<str:category_name>", views.category_listings, name="category_listings"),
    path("won_auctions", views.won_auctions, name="won_auctions"),
]
