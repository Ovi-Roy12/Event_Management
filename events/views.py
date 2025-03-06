from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from .models import Event, Category

# Home View (CBV)
class home(ListView):
    model = Event
    template_name = 'navlinks/home.html'
    context_object_name = 'events'

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        if search_query:
            return Event.objects.filter(name__icontains=search_query)
        return Event.objects.all()

# About Page (FBV )
def about(request):
    return render(request, 'navlinks/about.html')

# Contact Page (FBV)
def contact(request):
    return render(request, 'navlinks/contact.html')

# Event List View (CBV)
class event_list(ListView):
    model = Event
    template_name = 'event/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        events = Event.objects.select_related('category').prefetch_related('participants')
        category = self.request.GET.get('category')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if category:
            events = events.filter(category__name=category)
        if start_date and end_date:
            events = events.filter(date__range=[start_date, end_date])

        return events

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_participants'] = sum(event.participants.count() for event in self.get_queryset())
        return context

# Event Detail View (CBV)
class event_details(DetailView):
    model = Event
    template_name = 'event/event_details.html'
    context_object_name = 'event'

# Dashboard View (FBV remains unchanged)
def is_admin_or_organizer(user):
    return user.groups.filter(name__in=['Admin', 'Organizer']).exists()

def dashboard(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        date = request.POST.get('date', '').strip()
        time = request.POST.get('time', '').strip()
        location = request.POST.get('location', '').strip()
        category_id = request.POST.get('category')
        image = request.FILES.get('image')

        errors = []
        if not name:
            errors.append("Event name is required.")
        if not date:
            errors.append("Event date is required.")
        if not time:
            errors.append("Event time is required.")
        if not location:
            errors.append("Event location is required.")
        if not category_id:
            errors.append("Event category is required.")

        if errors:
            categories = Category.objects.all()
            events = Event.objects.all()
            return render(request, 'Dashboard/dashboard.html', {
                'categories': categories,
                'events': events,
                'errors': errors,  
            })
        try:
            category = Category.objects.get(id=category_id)
            Event.objects.create(
                name=name,
                description=description,
                date=date,
                time=time,
                location=location,
                category=category,
                image=image
            )
            return redirect('events:dashboard')
        except Category.DoesNotExist:
            return HttpResponseBadRequest("Invalid category selected")

    categories = Category.objects.all()
    events = Event.objects.all()
    return render(request, 'Dashboard/dashboard.html', {'categories': categories, 'events': events})

# Event Update View (CBV)
class update_event(UpdateView):
    model = Event
    fields = ['name', 'description', 'date', 'time', 'location', 'category', 'image']
    template_name = 'Dashboard/update_event.html'
    
    def get_success_url(self):
        return reverse_lazy('events:dashboard')

# Event Delete View (CBV)
class delete_event(DeleteView):
    model = Event
    template_name = 'Dashboard/event_confirm_delete.html'
    success_url = reverse_lazy('events:dashboard')

# RSVP to Event (FBV remains unchanged)
@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user in event.participants.all():
        messages.warning(request, "You have already RSVP'd for this event.")
    else:
        event.participants.add(request.user)
        messages.success(request, "You have successfully RSVP'd!")

        send_mail(
            'Event RSVP Confirmation',
            f'Thank you for RSVPing for {event.name} on {event.date} at {event.time}.',
            'no-reply@yourdomain.com',
            [request.user.email],
            fail_silently=False,
        )

    return redirect('event_detail', event_id=event.id)

# Cancel RSVP (FBV remains unchanged)
@login_required
def cancel_rsvp(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user in event.participants.all():
        event.participants.remove(request.user)
        messages.success(request, "Your RSVP has been canceled.")
    else:
        messages.warning(request, "You have not RSVP'd for this event.")

    return redirect('event_detail', event_id=event.id)

# Participant Dashboard View (FBV remains unchanged)
@login_required
def participant_dashboard(request):
    rsvp_events = request.user.rsvp_events.all()  
    return render(request, 'Dashboard/participant_dashboard.html', {'rsvp_events': rsvp_events})
