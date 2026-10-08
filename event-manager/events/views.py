from django.http import Http404
from django.shortcuts import render, redirect
from unicodedata import category

from events import data
from events.forms import EventForm


def index(request):
    return render(request,"events/base.html")

def event_list(request):
    events = data.list_events()
    status = request.GET.get('status')
    selected_category = request.GET.get('category')
    search = request.GET.get('search')
    total_events = len(events)
    total_active_events = len(data.active_events())
    total_close_events = len(data.close_events())

    filtered_list = events.copy()

    if status is not None:
        for item in events:
            if item["status"] != status:
                if item in filtered_list:
                    filtered_list.remove(item)
        if status == "all":
            filtered_list = events

    if selected_category is not None:
        for item in events:
            if item["category"] != selected_category:
                if item in filtered_list:
                    filtered_list.remove(item)
        if selected_category=="all":
            filtered_list = events

    if search is not None:
        for item in events:
            if item["name"].lower().find(search.strip().lower()) == -1 and item["location"].lower().find( search.strip().lower()) == -1:
                if item in filtered_list:
                    filtered_list.remove(item)


    return render(request,"events/event_list.html",{
        "data": filtered_list,
        "category": selected_category,
        "status": status,
        "total_events": total_events,
        "total_active_events": total_active_events,
        "total_close_events": total_close_events,}
    )

def event_detail(request,event_id):
    item = data.get_event(event_id)
    if item is None:
        raise Http404
    return render(request,"events/event_detail.html",{"data":item})
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            data.create_event(
                name = form.cleaned_data['name'],
                title = form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                location = form.cleaned_data['location'],
                category = form.cleaned_data['category'],
            )
            return redirect('events')
    else:
        form = EventForm()
    return render(request,"events/event_form.html",{"form":form})

def close_event(request, event_id):
    item = data.get_event(event_id)
    if item is None:
        raise Http404
    if request.method == "POST":
        data.close_event(event_id)
        return redirect('events')
    return render(request,"events/event_close.html",{"data":item})

def delete_event(request, event_id):
    item = data.get_event(event_id)
    if item is None:
        raise Http404
    if request.method == "POST":
        data.delete_event(event_id)
        return redirect('events')
    return render(request, 'events/confirm_event_delete.html', {'event': item})