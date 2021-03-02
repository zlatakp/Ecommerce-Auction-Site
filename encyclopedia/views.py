from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models

from . import util
app_name = 'wiki'

def index(request):
    """
    Returns search results matching the query
    """
    if request.method == "POST":
        q = request.POST.get("q")
        all_entries = util.list_entries()
        response = []
        for entry in all_entries:
            if entry.upper() == q.upper():
                response = redirect(('/wiki/'+entry))
            elif q.upper() in entry.upper():
                response.append(entry)
        return render(request, "encyclopedia/search.html", {
            "results": response
        })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def title(request, title):
    entry = util.get_entry(title)
    if entry == None:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
    else:
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "entry": entry
        })

def newpage(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        util.save_entry(title, content)
    else:
        return render(request, "encyclopedia/newpage.html", {
            "form": models.EntryForm(auto_id = True)
        })

        

