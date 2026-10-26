from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Skill

# --------------- LOGIN ---------------
def login_view(request):
    if request.user.is_authenticated:
        # Already logged in, go to dashboard
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


# --------------- SIGNUP ---------------
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})

        User.objects.create_user(username=username, email=email, password=password)
        return redirect('login')
    return render(request, 'signup.html')


# --------------- LOGOUT ---------------
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# --------------- DASHBOARD ---------------
@login_required
def dashboard(request):
    skills = Skill.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'skills': skills})


# --------------- ADD SKILL ---------------
@login_required
def add_skill(request):
    if request.method == "POST":
        Skill.objects.create(
            user=request.user,
            skill_name=request.POST['skill_name'],
            proficiency_level=request.POST['proficiency_level'],
            years_of_experience=request.POST['years_of_experience']
        )
        return redirect('dashboard')
    return render(request, 'add_skill.html')


# --------------- DELETE SKILL ---------------
@login_required
def delete_skill(request, skill_id):
    try:
        skill = Skill.objects.get(id=skill_id, user=request.user)
        skill.delete()
    except Skill.DoesNotExist:
        pass
    return redirect('dashboard')
