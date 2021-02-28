from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": util.get_entry(title))
    })