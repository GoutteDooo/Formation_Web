from django.shortcuts import render, redirect
from random import randint
import markdown2

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
    # Convertir le contenu Markdown en HTML
    html_content = markdown2.markdown(content)
    return render(request, "encyclopedia/page.html", {
        "title": title,
        "content": html_content
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

def edit(request, title):
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def save_edit(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect('entry', title=title)

def random(request):
    entries = util.list_entries()
    random_entry = randint(0, len(entries) - 1)
    return redirect('entry', title=entries[random_entry])