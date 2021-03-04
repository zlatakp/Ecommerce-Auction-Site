from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from django import forms
from random import randint

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
                return redirect('/wiki/'+entry)
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
    if request.method == "POST":
        data = {'title': title, 'content': util.get_entry(title)}
        submitted = request.POST
        form = models.EntryForm(submitted, initial = data)
        if form.has_changed():
            title = submitted.get("title")
            content = submitted.get("content")
            util.save_entry(title, content)
            return redirect("/wiki/"+title)
    else:
        entry = util.get_entry(title)
        if entry == None:
            return render(request, "encyclopedia/error.html", {
                "message": title + " page was not found."
            })
        else:
            form = models.EntryForm()
            form.fields["title"].initial = title
            form.fields["content"].initial = entry
            form.fields["title"].widget = forms.HiddenInput()
            form.fields["content"].widget = forms.HiddenInput()
            return render(request, "encyclopedia/title.html", {
                "title": title,
                "entry": entry,
                "form": form
            })

def newpage(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        all_entries = util.list_entries()
        for entry in all_entries:
            if entry.upper() == title.upper():
                return render(request, "encyclopedia/error.html", {
                    "message": title + " page already exists."
                })
        util.save_entry(title, content)
        return redirect("/wiki/"+title)
    else:
        return render(request, "encyclopedia/newpage.html", {
            "form": models.EntryForm(auto_id = True)
        })

def editpage(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        form = models.EntryForm(initial = {'title': title, 'content': content}, auto_id = True)
        return render(request, "encyclopedia/editpage.html", {
            "form": form,
            "title": title
        })
def random(request):
    all_entries = util.list_entries()
    low = 0
    high = len(all_entries) - 1
    title = all_entries[randint(low, high)]
    return redirect("/wiki/"+title)
    

        

