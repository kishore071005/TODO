from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task


def login_view(request):
    """Login page view"""
    if request.user.is_authenticated:
        return redirect('task_list')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task_list')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'app/login.html')


def register_view(request):
    """Register page view"""
    if request.user.is_authenticated:
        return redirect('task_list')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        
        # Basic validation
        if password != password2:
            messages.error(request, 'Passwords do not match')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters')
        else:
            # Create user
            user = User.objects.create_user(username=username, password=password, email=email)
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    
    return render(request, 'app/register.html')


def logout_view(request):
    """Logout user and redirect to login"""
    logout(request)
    return redirect('login')


@login_required
def task_list(request):
    """View to display all tasks for logged-in user"""
    tasks = Task.objects.filter(user=request.user)  # Only show user's tasks
    return render(request, 'app/task_list.html', {'tasks': tasks})


@login_required
def add_task(request):
    """View to add a new task for logged-in user"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        if title:  # Only create task if title is provided
            Task.objects.create(title=title, description=description, user=request.user)
            messages.success(request, 'Task added successfully!')
            return redirect('task_list')
    
    return render(request, 'app/add_task.html')


@login_required
def delete_task(request, task_id):
    """View to delete a task (only if it belongs to current user)"""
    try:
        task = Task.objects.get(id=task_id, user=request.user)  # Only allow deleting own tasks
        task.delete()
        messages.success(request, 'Task deleted successfully!')
    except Task.DoesNotExist:
        messages.error(request, 'Task not found or you do not have permission to delete it.')
    
    return redirect('task_list')