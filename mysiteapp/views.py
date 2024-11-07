# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import Message, ProgressUpdate, Meeting
from .forms import MessageForm, ProgressUpdateForm, MeetingForm,AdminUserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from datetime import datetime



def get_greeting():
    current_time = datetime.now().hour
    if current_time < 12:
        return "Good morning"
    elif 12 <= current_time < 18:
        return "Good Afternoon"
    else:
        return "Good Evening"


def is_staff_user(user):
    return user.is_staff

def is_parent(user):
    return user.role =='parent'

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
    greeting = get_greeting()
    context = {
        'greeting': greeting,
        'user_name': request.user.username, 
    }
    return render(request, 'mysiteapp/base.html',context)

@user_passes_test(is_parent)
@login_required
def messages_view(request):
    messages_received = Message.objects.filter(receiver=request.user)
    messages_sent = Message.objects.filter(sender=request.user)
    User = get_user_model()
    users = User.objects.all()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = User.objects.get(id=request.POST['receiver'])
            message.save()
            return redirect('messages')
    else:
        form = MessageForm()
    return render(request, 'mysiteapp/messages.html', {
        'messages_received': messages_received, 
        'messages_sent': messages_sent,
          'form': form,
          'users_list': users})

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
        else:
            messages.info(request,'Please register before logging in to usse the application')
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
        else:
            messages.info(request,'Please register before logging in to usse the application')
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
            return redirect('messages')  
        else:
            messages.info(request,'Please register before logging in to usse the application')
            return render(request, 'mysiteapp/login.html', {'error': 'Invalid credentials'})
    return render(request, 'mysiteapp/login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')