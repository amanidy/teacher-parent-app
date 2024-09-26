from django.db import models
from django.contrib.auth.models import AbstractUser

# User model corresponding to the 'users' table
class User(AbstractUser):
    ROLE_CHOICES = [
        ('parent', 'Parent'),
        ('teacher', 'Teacher')
    ]
    
    
    email = models.EmailField(blank=True,null=True)
    role = models.CharField(max_length=7, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    parent_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username


# Message model corresponding to the 'messages' table
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    reply_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')


    class Meta:
        db_table = 'messages'  # Reference to the existing table in MySQL

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}"


# Progress updates model corresponding to the 'progress_updates' table
class ProgressUpdate(models.Model):
    student_name = models.CharField(max_length=100)
    update_text = models.TextField()
    teacher = models.ForeignKey(User, related_name='teacher_updates', on_delete=models.CASCADE)
    parent = models.ForeignKey(User, related_name='parent_updates', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'progress_updates'  # Reference to the existing table in MySQL

    def __str__(self):
        return f"Progress update for {self.student_name}"


# Meeting model corresponding to the 'meetings' table
class Meeting(models.Model):
    teacher = models.ForeignKey(User, related_name='teacher_meetings', on_delete=models.CASCADE)
    parent = models.ForeignKey(User, related_name='parent_meetings', on_delete=models.CASCADE)
    meeting_date = models.DateTimeField()
    agenda = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'meetings'  # Reference to the existing table in MySQL

    def __str__(self):
        return f"Meeting between {self.teacher.username} and {self.parent.username} on {self.meeting_date}"


class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)  # Adjust the length as needed

    def __str__(self):
        return self.name