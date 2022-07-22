from django.urls import path
from . import views

urlpatterns = [
    path("",views.hi,name="greeting"),
    path("<str:name>",views.greet,name="greet"),
]
