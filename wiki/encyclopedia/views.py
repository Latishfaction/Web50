from django.shortcuts import render
import markdown
from . import util
from django import forms

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
        "html":validate_entry(util.get_entry(title.capitalize()),title),
    })
def validate_entry(entry,title):
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

