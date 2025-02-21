from django.urls import path
from events import views

app_name = 'events'

urlpatterns =[
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('event_list/', views.event_list, name='event_list'),
    path('event/<int:event_id>/', views.event_details, name='event_details'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update-event/<int:event_id>/', views.update_event, name='update_event'),
    path('delete-event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('rsvp/<int:event_id>/', views.rsvp_event, name='rsvp_event'),
    path('cancel-rsvp/<int:event_id>/', views.cancel_rsvp, name='cancel_rsvp'),
    path('participant-dashboard/', views.participant_dashboard, name='participant_dashboard'),
]