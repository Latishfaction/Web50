from django.shortcuts import render

# Create your views here.
from datetime import datetime

def index(request):
    now = datetime.now()
    return render(request,"newyear/index.html",{
        "newyear" : now.day == 1 and now.month ==1
    })

    