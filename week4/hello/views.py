from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def hi(request):
    #return HttpResponse("Hello World")
    return render(request,"hello/index.html")

def greet(request,name):
    #return HttpResponse(f"Hello {name.capitalize()}")
    return render(request, "hello/greet.html",{
        "name" : name.capitalize()
    })


