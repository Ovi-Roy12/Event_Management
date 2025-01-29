from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from .models import Event,Participant,Category
from django.urls import reverse
from django.http import HttpResponseBadRequest
# Create your views here.

def home(request):
    search_query = request.GET.get('search', '') 
    
    if search_query:
        events = Event.objects.filter(name__icontains=search_query)
    else:
        events = Event.objects.all()
    return render(request, 'home.html',{'events': events})

def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event/event_details.html', {'event': event})

def event_list(request):
    events = Event.objects.select_related('category') 
    events = Event.objects.prefetch_related('participants')
    total_participants = Event.objects.aggregate(total=Count('participants'))['total']
    category = request.GET.get('category') 
    start_date = request.GET.get('start_date')  
    end_date = request.GET.get('end_date')  
    # Apply filters
    if category:
        events = events.filter(category__name=category) 
    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date]) 

    return render(request, 'event/event_list.html', {'events': events,'total_participants': total_participants})

def dashboard(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        date = request.POST.get('date', '').strip()
        time = request.POST.get('time', '').strip()
        location = request.POST.get('location', '').strip()
        category_id = request.POST.get('category')  # This might not exist
        image = request.FILES.get('image')

        # Validate required fields
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

#update Event
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        event.name = request.POST.get('name')
        event.description = request.POST.get('description')
        event.date = request.POST.get('date')
        event.time = request.POST.get('time')
        event.location = request.POST.get('location')
        event.category = Category.objects.get(id=request.POST.get('category'))
        event.image = request.FILES.get('image', event.image) 
        event.save()
        return redirect('events:dashboard')
    
    return render(request, 'Dashboard/update_event.html', {'event': event, 'categories': categories})

# Delete Event
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('events:dashboard')

