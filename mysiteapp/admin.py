from django.contrib import admin
from .models import User, Message, ProgressUpdate, Meeting



admin.site.register(User)
admin.site.register(Message)
admin.site.register(ProgressUpdate)
admin.site.register(Meeting)
