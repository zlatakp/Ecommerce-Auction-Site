from django.urls import path

from . import views
from django.conf.urls import url
urlpatterns = [
    path('', views.index, name="index"),
    path('<str:title>/', views.title, name = "title")
]
