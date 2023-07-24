from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Category, Bid, Comment


def index(request):
    listings = Listing.objects.filter(active=True).all()
    return render(request, "auctions/index.html", {
        "listings":listings,
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def add(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        image_url = request.POST["image-url"]
        starting_bid = float(request.POST["starting-bid"])
        category = request.POST['category']
        new_listing = Listing(
            title=title,
            description=description,
            image=image_url,
            price = starting_bid,
            category = Category.objects.get(name=category),
            owner = request.user
        )
        new_listing.save()
        return HttpResponseRedirect(reverse('index'))
    available_categories = Category.objects.all()
    return render(request, "auctions/add.html", {
        "categories": available_categories,
    })


def view_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    comments = Comment.objects.filter(listing=listing)
    if request.user.is_authenticated:
        bidding = Bid.objects.filter(item=listing)
        user_bidding = bidding.filter(bidder=request.user)
        max_bid = None
        if bidding:
            max_bid = 0
            for bid in bidding:
                if bid.quantity > max_bid:
                    max_bid = bid.quantity
    
        if listing.winner == request.user:
            winner_is_the_user = True
        else:
            winner_is_the_user = False
        the_owner = listing.owner
        if the_owner == request.user:
            close_auction_deal = True
        else:
            close_auction_deal = False
        if request.user in listing.watched_at.iterator():
            return render(request, "auctions/view.html", {
                "watched":True,
                "listing":listing,
                "max_bid":max_bid,
                "user_bid": user_bidding,
                "close_auction": close_auction_deal,
                "won_the_auction":winner_is_the_user,
                "comments":comments,

            })
        else:
            return render(request, "auctions/view.html", {
                "watched":False,
                "listing":listing,
                "max_bid":max_bid,
                "user_bid": user_bidding,
                "close_auction": close_auction_deal,
                "won_the_auction":winner_is_the_user,
                "comments":comments,

            })
    else:
        return render(request, "auctions/view.html", {
            "listing":listing,
            "comments":comments,
        })
        

@login_required
def add_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.watched_at.add(request.user)
    listing.save()
    return view_listing(request, listing_id)

@login_required
def remove_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.watched_at.remove(request.user)
    listing.save()
    return view_listing(request, listing_id)

@login_required
def bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bidding = Bid.objects.filter(item=listing)
    max_bid = None
    if bidding is not None:
        max_bid = 0
        for bids in bidding:
            if bids.quantity > max_bid:
                max_bid = bids.quantity
    
    users_bid = bidding.filter(bidder = request.user)

    if request.method == "POST":
        the_bid = float(request.POST["my_bid"])
    
        if the_bid > max_bid and the_bid > listing.price:
            
            new_bid = Bid(bidder=request.user, quantity=the_bid, item=listing)
            new_bid.save()
            return view_listing(request, listing_id)
        else:
            if bidding is None:
                return render(request, "auctions/bid.html", {
                    "listing":listing,
                    "message": "Your bid should be higher than the current highest bid and starting price",
                })
            else:
                max_bid = 0
                for bids in bidding:
                    if bids.quantity > max_bid:
                        max_bid = bids.quantity
                return render(request, "auctions/bid.html", {
                    "listing":listing,
                    "max_bid":max_bid,
                    "message": "Your bid should be higher than the current highest bid and starting price",
                })
                    
    if bidding is not None:
        return render(request, "auctions/bid.html", {
            "listing": listing,
            "max_bid": max_bid,
            "user_bid": users_bid,
        })
    else:

        return render(request, "auctions/bid.html", {
            "listing": listing,
            "user_bid": users_bid,
        })

@login_required
def close_auction(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.active = False
    all_bid = Bid.objects.filter(item=listing)
    if all_bid is not None:
        max_bid = 0
        for bid in all_bid:
            if bid.quantity > max_bid:
                max_bid = bid.quantity
        the_winner = None
        for bid in all_bid:
            if bid.quantity == max_bid:
                the_winner = bid.bidder
        listing.winner = the_winner
    else:
        listing.winner = None
    listing.save()
    return HttpResponseRedirect(reverse('index'))

@login_required
def watchlist(request):
    watchlisted_listings = Listing.objects.filter(watched_at=request.user)
    return render(request, "auctions/watchlist.html", {
        "listings": watchlisted_listings,
    })

@login_required
def comment(request, listing_id):
    if request.method == "POST":
        coment = request.POST["content"]
        listing = Listing.objects.get(pk=listing_id)
        new_comment = Comment(commentor=request.user, comment=coment, listing=listing)
        new_comment.save()
        return view_listing(request, listing_id)
        

def categories(request):
    cats = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories":cats,
    })

def category_listings(request, category_name):
    category = Category.objects.get(name=category_name)
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/category_detail.html", {
        "listings":listings,
        "category": category.name
    })

@login_required
def won_auctions(request):
    won_listings = Listing.objects.filter(winner=request.user)
    return render(request, "auctions/won_auctions.html", {
        "listings":won_listings,
    })