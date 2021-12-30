from django.shortcuts import render
import random
from django import forms
from . import util
import markdown2

class Create(forms.Form):
    title = forms.CharField(label='Title')
    text_box = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder':'Enter text here'}))

class Edit(forms.Form):
    text_box = forms.CharField(label='', widget=forms.Textarea())

class Search(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class': 'searchbar', 'placeholder': 'Search'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        'form': Search(),
    })

def newpage(request):
    if request.method == 'POST':
        new_entry = Create(request.POST)
        if new_entry.is_valid():
            title = new_entry.cleaned_data['title']
            text = new_entry.cleaned_data['text_box']
            if title not in util.list_entries():
                util.save_entry(title, text)
                return render(request, "encyclopedia/entry.html", {
                    'title': title,
                    'text': markdown2.markdown(util.get_entry(title)),
                    'form': Search(),
                })
            else:
                return render(request, 'encyclopedia/error.html', {
                    'error': 'This entry has already been made!',
                    'form': Search(),
                })

    return render(request, 'encyclopedia/newpage.html', {
        'create': Create(),
        'form': Search(),
    })


def entry(request, entry):
    if entry in util.list_entries():
        text = util.get_entry(entry)
        return render(request, "encyclopedia/entry.html", {
            'title': entry,
            'text': markdown2.markdown(text),
            'form': Search(),
        })
    else: 
        return render(request, "encyclopedia/error.html", {
        'error': 'Invalid Entry Title',
        'form': Search(),
    })


def edit(request, entry):
    if request.method == 'POST':
        new_entry = Edit(request.POST)
        if new_entry.is_valid():
            text = new_entry.cleaned_data['text_box']
            util.save_entry(entry, text)
            return render(request, 'encyclopedia/entry.html', {
                'title': entry,
                'text': markdown2.markdown(util.get_entry(entry)),
                'form': Search(),
            })
        
    else:
        text = util.get_entry(entry)
        
        return render(request, 'encyclopedia/edit.html', {
            'title': entry,
            'edit': Edit(initial={'text_box': text}),
            'form': Search(),
        })


def randomPage(request):
    entries = util.list_entries()
    e = random.choice(entries)
    return entry(request, e)


def search(request):
    searched = Search(request.POST)
    if searched.is_valid():
        search = searched.cleaned_data['search']
        entries = util.list_entries()
        matched = []
        for x in entries:
            if search.lower() == x.lower():
                text = markdown2.markdown(util.get_entry(x))
                return render(request, 'encyclopedia/entry.html', {
                    'title': x,
                    'text': text,
                    'form': Search(),
                })
            if search.lower() in x.lower():
                matched.append(x)
        return render(request, 'encyclopedia/search.html', {
            'title': search,
            'matched': matched,
            'form': Search(),
        })