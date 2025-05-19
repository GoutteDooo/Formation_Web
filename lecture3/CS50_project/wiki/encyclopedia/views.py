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
    query = request.GET.get("q", "")
    if not query:
        return render(request, "encyclopedia/search.html", {
            "query": "",
            "entries": [],
            "message": "Please enter a search term"
        })
    
    entries = []
    for entry in util.list_entries():
        if query.lower() in entry.lower():
            entries.append(entry)
    
    if not entries:
        message = f"No results found for '{query}'"
    else:
        message = f"Results for '{query}'"
    
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "entries": entries,
        "message": message
    })