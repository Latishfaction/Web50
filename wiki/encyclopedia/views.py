from django.shortcuts import render
import markdown
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
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
