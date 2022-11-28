from django.shortcuts import render
import markdown
from . import util
from django import forms
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.urls import reverse

class search_entry(forms.Form):
    title = forms.CharField(label="entry:")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form":search_entry(),
    })

def entryPage(request,title):
    return render(request,"encyclopedia/entries.html",{
        "title":title.capitalize(),
        "html":validate_entry(util.get_entry(title.capitalize())),
        "form":search_entry(),
    })
#convert markdown into HTML
def validate_entry(entry):
    if(entry == None):
        return False
    else:
        return markdown.markdown(entry)

# searching for entries
def search(request):
    title = search_entry(request.GET)
    if title.is_valid():
        entries=[]
        title=(title.cleaned_data["title"]).lower()

        for x in util.list_entries():
            if title in x.lower():
                entries.append(x)
        return render(request,"encyclopedia/search.html",{
        "list":entries})


#create new page
def create(request):
    if request.method =="POST":
        raw_data = request.POST
        if is_valid(raw_data):
            fileName = raw_data['filename'].capitalize()
            content = raw_data['content']
            content = content.encode(encoding="UTF-8")

            if default_storage.exists("entries/"+fileName+".md"):
                #show error message
                return render(request,"encyclopedia/create.html",{
                    "error":True,
                    "form":search_entry()
                })
            else:
                util.save_entry(fileName, content)
                #redirect to the index page
                return HttpResponseRedirect(reverse("wiki:index"))
    return render(request,"encyclopedia/create.html",{
        "error":False,
        "form":search_entry(),
    })

# for checking the blank fileds on textfiled and textarea
def is_valid(raw_data):
    filename = "".join(raw_data['filename'])

    content = "".join(raw_data['content'])

    space = filename.isspace() and content.isspace() and filename[0].isspace() and content[0].isspace()
    # convert the field data into string and then check the length
    if len(filename)>1 and len(content) >1 and not(space):
        return True
    else:
        return False


# edit page
def edit(request):
    if request.method == "GET":
        #making title accessible to the GET and POST method
        global title
        title = request.GET['title_name']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "title":title,
            "markdown":content,
            "form":search_entry()
        })
    if request.method =="POST":
        content = request.POST['content']
        util.save_entry(title,content)
        return HttpResponseRedirect(reverse("wiki:index"))

# random
import random
def random_entry(request):
    titles = util.list_entries()
    title = random.choice(titles)
    entry = validate_entry(util.get_entry(title))
    return render(request,"encyclopedia/random.html",{
        "entry":entry,
        "form":search_entry()
    })