from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User, Category, Listing
from django import forms

class NewListing(forms.Form):
    categories = list(Category.objects.values_list())
    title = forms.CharField(label = "Title", max_length = 100, required = True)
    start_bid = forms.DecimalField(label = "Starting Bid", decimal_places = 2, required = True)
    category = forms.ChoiceField(widget = forms.Select, choices = categories, label = "Category" )
    description = forms.CharField(widget = forms.Textarea)
    url = forms.URLField(required = False)
    

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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
            listing = Listing(title = title, start_bid = start_bid, url = url, description = description, category = category)
            listing.save()
            return redirect("listing/"+str(listing.id))
    else:
        form = NewListing()
        categories = Category.objects.all()
        return render(request, "auctions/createlisting.html", {
            "categories": categories,
            "form": form
        })
def listing(request, list_id):
    listing = Listing.objects.get(id = list_id)
    user_id = request.user.id
    watching = User.objects.get(id = user_id).watching.values_list
    return render(request, "auctions/listing.html", {
        "title": listing.title,
        "listing_id": listing.id,
        "start_bid": "${:,.2f}".format(listing.start_bid),
        "category": listing.category,
        "description": listing.description,
        "url": listing.url,
        "test": watching
    })

    
def add(request, list_id):
    if request.method == "POST":
        user_id = request.user.id
        listing = Listing.objects.get(id = list_id)
    else:
        return HttpResponseRedirect(reverse("listing", args = (list_id,) ))

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
