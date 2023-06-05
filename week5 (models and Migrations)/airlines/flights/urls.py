from . import views 
from django.urls import path 

app_name='flights_data'

urlpatterns=[
    path("",views.index,name="index"),
    path("<int:flight_id>",views.flight,name="flight_details"),
    path("<int:flight_id>/book",views.book,name="book"),
]