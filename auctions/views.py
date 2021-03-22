from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User, Category, Listing, Bid
from django import forms

class NewListing(forms.Form):
    categories = list(Category.objects.values_list())
    title = forms.CharField(label = "Title", max_length = 100, required = True)
    start_bid = forms.DecimalField(label = "Starting Bid", decimal_places = 2, required = True)
    category = forms.ChoiceField(widget = forms.Select, choices = categories, label = "Category" )
    description = forms.CharField(widget = forms.Textarea)
    url = forms.URLField(required = False)


class NewBid(forms.Form):
    bid = forms.DecimalField(label = "Your Bid", decimal_places=2)
    def __init__(self, *args, **kwargs):
        try:
            current_min = kwargs.pop('current_min')
        except KeyError:
            current_min = 0
        super(NewBid, self).__init__(*args, **kwargs)
        self.fields['bid'].widget.attrs['min'] = float(current_min)



def index(request):
    if request.method == "POST":
        list_id = request.POST.get("list_id")
        listing_set = Listing.objects.filter(id = list_id)
        listing = listing_set[0]
        bid_set = Bid.objects.filter(listing = listing)
        bid = bid_set[0]
        bidder = bid.bidder
        listing_set.update(status = 'inactive', winner = bidder)

        return render(request, "auctions/index.html", {
            "title": "Active Listings",
            "listings": Listing.objects.filter(status = 'active')
            })
    else:
        return render(request, "auctions/index.html", {
            "title": 'Active Listings',
            "listings": Listing.objects.filter(status = 'active')
            })

def create_new(request):

    if request.method == "POST":
        form = NewListing(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            start_bid = form.cleaned_data["start_bid"]
            description = form.cleaned_data["description"]
            category_id = form.cleaned_data["category"]
            category = Category.objects.get(id = category_id)
            url = form.cleaned_data["url"]
            owner = User.objects.get(id = request.user.id)
            listing = Listing(title = title, owner = owner, start_bid = start_bid, url = url, description = description, category = category)
            listing.save()
            bid = Bid(listing = listing, current_bid = start_bid)
            bid.save()

            return HttpResponseRedirect(reverse("listing", args = (listing.id, )))
    else:
        form = NewListing()
        categories = Category.objects.all()
        return render(request, "auctions/createlisting.html", {
            "categories": categories,
            "form": form
        })
def listing(request, list_id):
    if request.method == "POST":
        bidform = NewBid(request.POST)
        if bidform.is_valid():
            listing = Listing.objects.get(id = list_id)
            bidded = bidform.cleaned_data['bid']
            bid = Bid.objects.get(listing = listing)
            current_bid = bid.current_bid
            if bidded > current_bid:
                user = User.objects.get(id = request.user.id)
                Bid.objects.filter(listing = listing).update(current_bid = bidded, bidder = user)  
                watching_status = user.watchedby.filter(id = list_id).exists()
                form = NewBid(current_min = bidded)
                return HttpResponseRedirect(reverse('listing', args = (list_id, )))
            return HttpResponseRedirect(reverse("listing", args = (list_id,)))

    else:
        listing = Listing.objects.get(id = list_id)
        bid = Bid.objects.get(listing = listing)
        user = User.objects.get(id = request.user.id)
        owner_status = listing.owner == user
        watching_status = user.watchedby.filter(id = list_id).exists()
        form = NewBid(current_min = bid.current_bid)
        won = False
        if listing.winner == user:
            won = True
        return render(request, "auctions/listing.html", {
            "owner_status": str(owner_status).lower(),
            "form": form,
            "listing": listing,
            "won": won,
            "start_bid": "${:,.2f}".format(listing.start_bid),
            "current_bid": "${:,.2f}".format(bid.current_bid),
            "watching_status": str(watching_status).lower()
        })

    
def add(request, list_id):
    if request.method == "POST":
        user = User.objects.get(id = request.user.id)
        listing = Listing.objects.get(id = list_id)
        listing.watched.add(user)
        return HttpResponseRedirect(reverse("listing", args = (list_id,)))
    else:
        return HttpResponseRedirect(reverse("listing", args = (list_id,) ))

def remove(request, list_id):
    if request.method == "POST":
        user = User.objects.get(id = request.user.id)
        listing = Listing.objects.get(id = list_id)
        listing.watched.remove(user)
        return HttpResponseRedirect(reverse("listing", args = (list_id,)))
    else:
        return HttpResponseRedirect(reverse("listing", args = (list_id,)))

def watchlist(request):
    if request.method == "GET":
        user = User.objects.get(id = request.user.id)
        watchlist = user.watchedby.filter(status = 'active')
        return render(request, "auctions/watchlist.html", {
            "watchlist": watchlist
        })

def categories(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/categories.html", {
            "categories": categories
        })

def category_listing(request, cat_id):
    if request.method == "GET":
        category = Category.objects.get(id = cat_id)
        listings = category.category_listing.filter(status = 'active')
        return render(request, "auctions/index.html", {
            "title": category.name,
            "listings": listings
        })


def won(request):
    user  = User.objects.get(id = request.user.id)
    listings = user.wonitems.all()
    return render(request, "auctions/index.html", {
        "title": "Won Auctions",
        "listings": listings
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
