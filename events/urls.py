from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.event_list_create, name='event-list-create'),
]