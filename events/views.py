import calendar
from datetime import date
from calendar import HTMLCalendar
from django.shortcuts import render
from .models import Event

def calendar_view(request):
    today = date.today()
    year = today.year
    month = today.month
    cal = HTMLCalendar().formatmonth(year, month)
    events = Event.objects.filter(date__month=month)
    return render(request, 'events/calendar.html', {
        'calendar': cal,
        'events': events,
    })