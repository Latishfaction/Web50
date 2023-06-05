from django.urls import path

from . import views


app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("search/",views.search,name="search"),
    path("<str:title>",views.entryPage,name="page"),
    path("create/",views.create,name="create"),
    path("edit/",views.edit,name="edit"),
    path("random/",views.random_entry,name="random")
]
