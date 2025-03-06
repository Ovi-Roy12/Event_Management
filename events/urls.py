from django.urls import path
from .views import home, event_list, event_details, update_event, delete_event, about, contact, dashboard, rsvp_event, cancel_rsvp, participant_dashboard

app_name = 'events'

urlpatterns = [
    path('', home.as_view(), name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('dashboard/', dashboard, name='dashboard'),
    path('events/', event_list.as_view(), name='event_list'),
    path('event/<int:pk>/', event_details.as_view(), name='event_details'),
    path('event/update/<int:pk>/', update_event.as_view(), name='update_event'),
    path('event/delete/<int:pk>/', delete_event.as_view(), name='delete_event'),
    path('event/<int:event_id>/rsvp/', rsvp_event, name='rsvp_event'),
    path('event/<int:event_id>/cancel_rsvp/', cancel_rsvp, name='cancel_rsvp'),
    path('participant/dashboard/', participant_dashboard, name='participant_dashboard'),
]
