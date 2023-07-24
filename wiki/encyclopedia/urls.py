from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.view_wiki, name="view_wiki"),
    path("search", views.search, name="search"),
    path("add", views.add_wiki, name="add_wiki"),
    path("edit/<str:title>", views.edit_wiki, name="edit"),
    path("random", views.random_wiki, name="random"),
]
