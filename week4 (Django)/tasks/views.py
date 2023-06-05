from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

# creating form class with text field named tasks

class Tasks(forms.Form):
    # forms fields
    task = forms.CharField(label='Tasks')
    # priopity = forms.IntegerField(label='Priority',min_value=1,max_value=5)

def index(request):
    # checking tasks is in request.sessions, if not then create an empty list with that name
    if 'tasks' not in request.session:
        request.session['tasks'] = []
    # returning index.html by passing the elements of request.sessions as 'tasks'
    return render(request,'tasks/index.html',{
        "tasks":request.session['tasks']
    })

def add(request):
    # Whenever we are not requesting server then 'GET' request is used, that is why we are checking the request type

    # checking for 'POST' request
    if request.method == 'POST':
        # request.POST is used to get the data that user is trying to put in the server
        form_data = Tasks(request.POST)

        # checking for server validation
        if form_data.is_valid():
            # getting the exact value inside the text-felid which refers to the class Tasks(forms.form)
            task = form_data.cleaned_data['task']
            
            # storing the above retrived tasks in the session
            request.session['tasks'] += [task]

            # redirects to the index.html
            #reverse used to reverse the name into url
            return HttpResponseRedirect(reverse('tasks:index'))
        else:
            # if the form is not valid , then return the user the form that he filed earlier

            return render(request,'tasks/add.html',{
                'form':form_data
            })
    
    # if the request is 'GET' , send the add.html file, by sending form data in Tasks class, it simply provies blank form
    return render(request,'tasks/add.html',{
        'form':Tasks()
    })

# delete the entire session and redirect the user to index.html
def deleteSessions(request):
    del request.session['tasks']
    return HttpResponseRedirect(reverse('tasks:index'))