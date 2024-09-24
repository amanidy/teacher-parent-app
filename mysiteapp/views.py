# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import Message, ProgressUpdate, Meeting
from .forms import MessageForm, ProgressUpdateForm, MeetingForm,AdminUserCreationForm


def is_staff_user(user):
    return user.is_staff

def register_user(request):
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = AdminUserCreationForm()
    
    return render(request, 'mysiteapp/register_user.html', {'form': form})

@login_required
def base(request):
    return render(request, 'mysiteapp/base.html')

@login_required
def messages_view(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('messages')
    
    messages = Message.objects.all()
    form = MessageForm()
    return render(request, 'mysiteapp/messages.html', {'messages': messages, 'form': form})

# Progress updates view - protected
@login_required
def progress_updates_view(request):
    if request.method == 'POST':
        form = ProgressUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.teacher = request.user
            update.save()
            return redirect('progress_updates')
    
    updates = ProgressUpdate.objects.all()
    form = ProgressUpdateForm()
    return render(request, 'mysiteapp/progress_updates.html', {'updates': updates, 'form': form})

# Meetings view - protected
@login_required
def meetings_view(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.teacher = request.user
            meeting.save()
            return redirect('meetings')
    
    meetings = Meeting.objects.all()
    form = MeetingForm()
    return render(request, 'mysiteapp/meetings.html', {'meetings': meetings, 'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  
        else:
            return render(request, 'mysiteapp/login.html', {'error': 'Invalid credentials'})
    return render(request, 'mysiteapp/login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')