from django.shortcuts import render, redirect
from .models import Event
from datetime import date
from calendar import HTMLCalendar
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EventSerializer

class EventCalendar(HTMLCalendar):
    def __init__(self, events):
        super().__init__()
        self.events_by_date = self.group_by_day(events)

    def group_by_day(self, events):
        data = {}
        for event in events:
            day = event.date.day
            if day in data:
                data[day].append(event)
            else:
                data[day] = [event]
        return data

    def formatday(self, day, weekday):
        if day == 0:
            return '<td></td>'
        cssclass = self.cssclasses[weekday]
        events = self.events_by_date.get(day, [])
        badge = f'<span class="badge">{len(events)}</span>' if events else ''
        return f'<td class="{cssclass}"><div>{day}{badge}</div></td>'

def calendar_view(request):
    today = date.today()
    year = today.year
    month = today.month

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        event_date = request.POST.get("date")
        if title and event_date:
            Event.objects.create(title=title, description=description, date=event_date)
            return redirect('/')

    events = Event.objects.filter(date__month=month)
    cal = EventCalendar(events).formatmonth(year, month)
    return render(request, 'events/calendar.html', {
        'calendar': cal,
        'events': events,
    })

@api_view(['GET', 'POST'])
def event_list_create(request):
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)