from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . import util
import markdown2
import random


def index(request):
    title = request.GET.get("q")
    print(title)
    entries = util.list_entries()
    print(entries)
    if not title:
        return render(request, "encyclopedia/index.html", {
            "entries": entries
        })
    return HttpResponseRedirect(reverse('search'))
    
def view_wiki(request, title):

    if util.get_entry(title) is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Your requested page was not found",
        })
    else:
        wiki = util.get_entry(title)
        markdowner = markdown2.Markdown()
        
        return render(request, "encyclopedia/wiki.html",{
            "content": markdowner.convert(wiki),
            "title": title
        })


def search(request):
    if request.method == "POST":
        entry = request.POST['q']
        wiki = util.get_entry(entry)
        if wiki is not None:
            markdowner = markdown2.Markdown()
            return render(request, "encyclopedia/wiki.html",{
                "content": markdowner.convert(wiki),
                "title": entry
            })
        else:
            recom = []
            all_entries = util.list_entries()
            for single_entry in all_entries:
                if entry.lower() in single_entry.lower():
                    recom.append(single_entry)
            
            return render(request, "encyclopedia/results_page.html", {
                "entries": recom,
                "entry": entry,
            })
                    

def add_wiki(request):
    if request.method == "GET":
        return render(request, "encyclopedia/add_wiki.html")
    elif request.method == "POST":
        title = request.POST['title']
        entries = util.list_entries()
        for entry in entries:
            if title.lower() == entry.lower():
                return render(request, "encyclopedia/add_wiki.html", {
                    "message": f"There is an entry with the title of {title}."
                })
        content = request.POST['content']
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse('index'))

def edit_wiki(request, title):
    if request.method == "GET":
        entry = util.get_entry(title)
        print(entry)
        return render(request, "encyclopedia/edit_wiki.html", {
            "content": entry,
            "title": title,
        })
    else:
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        return view_wiki(request, title)


def random_wiki(request):
    entries = util.list_entries()
    random_index = random.randint(0, len(entries) - 1)
    return view_wiki(request, entries[random_index])