# forms.py

from django import forms
from .models import Message, ProgressUpdate, Meeting
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import User

class AdminUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('role', 'parent_to')

    def save(self, commit=True):
        user = super().save(commit=False)

        # Check the role and set is_staff accordingly
        if user.role == 'teacher':
            user.is_staff = True  # Teachers are staff
        else:
            user.is_staff = False  
        
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
