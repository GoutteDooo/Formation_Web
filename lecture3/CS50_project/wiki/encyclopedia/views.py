from django.shortcuts import render, redirect

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
        return redirect('index')
    
    entries = []
    for entry in util.list_entries():
        if query.lower() in entry.lower():
            entries.append(entry)
    
    if not entries:
        message = f"No results found for '{query}'"
    else:
        message = f"Results for '{query}'"

    if len(entries) == 1 and entries[0].lower() == query.lower():
        return redirect('entry', title=entries[0])

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "entries": entries,
        "message": message
    })

def new(request):
    return render(request, "encyclopedia/new.html")

def save_new(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        #Search if the entry already exists
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/new.html", {
                "error": "Entry already exists"
            })
        util.save_entry(title, content)
        return render(request, "encyclopedia/new.html", {
            "message": "Page added successfully !"
        })

def edit(request):
    title = request.GET.get("title")
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def save_edit(request):
    pass