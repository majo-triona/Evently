from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view),
    path('api/', views.event_list_create),
]