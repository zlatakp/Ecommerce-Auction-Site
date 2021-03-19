from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.create_new, name = "newlisting"),
    path("listing/<int:list_id>/", views.listing, name = "listing"),
    path("listing/<int:list_id>/add", views.add, name = "add"),
    path("listing/<int:list_id>/remove", views.remove, name = "remove"),
    path("watchlist/", views.watchlist, name = "watchlist"),
    path("categories/", views.categories, name = "categories"),
    path("categories/<int:cat_id>/", views.category_listing, name = "category_listing")
]
