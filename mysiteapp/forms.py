# forms.py

from django import forms
from .models import Message, ProgressUpdate, Meeting
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True  
        if commit:
            user.save()
        return user

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']  
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Type your message here...', 'rows': 4}),
        }

class ProgressUpdateForm(forms.ModelForm):
    class Meta:
        model = ProgressUpdate
        fields = ['student_name', 'update_text', 'parent']  
        widgets = {
            'update_text': forms.Textarea(attrs={'placeholder': 'Enter progress update...', 'rows': 4}),
        }

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['parent', 'meeting_date', 'agenda']  # Specify fields for the meeting form
        widgets = {
            'agenda': forms.Textarea(attrs={'placeholder': 'Enter agenda for the meeting...', 'rows': 4}),
        }
