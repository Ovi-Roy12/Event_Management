from django.contrib.auth.models import User,Group
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("users:register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("users:register")

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )
        user.save()

        # Assign default role (Participant)
        participant_group = Group.objects.get(name="Participant")
        user.groups.add(participant_group)

        messages.success(request, "Account created successfully! Please log in.")
        return redirect("users:login")

    return render(request, "registration/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")  
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!") 
            return redirect('events:home')  
        else:
            messages.error(request, "Invalid username or password!")  

    return render(request, "registration/login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect("users:login")  


def admin_dashboard(request):
    return render(request, "admin-dashboard.html")

