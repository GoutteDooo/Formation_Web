from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/page.html", {
            "title": "No page here :(",
            "content": "Page not found"
        })
    return render(request, "encyclopedia/page.html", {
        "title": title,
        "content": content
    })

def search(request):
    query = request.POST.get("q")
    print(query)