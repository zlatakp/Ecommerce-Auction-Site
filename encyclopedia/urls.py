from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("newpage/", views.newpage, name = 'newpage'),
    path('editpage/', views.editpage, name = 'editpage'),
    path("<str:title>/", views.title, name = 'title')
    
]
