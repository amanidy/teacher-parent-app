from django.contrib import admin
from .models import User, Message, ProgressUpdate, Meeting
from django.contrib import messages
from .forms import AdminUserCreationForm  # Make sure this form is defined in forms.py

class UserAdmin(admin.ModelAdmin):
    form = AdminUserCreationForm
    list_display = ['username', 'role', 'parent_to', 'is_staff', 'is_superuser']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    
    def send_message_to_parent(self, request, queryset):
        parents = queryset.filter(role='parent')
        messages_sent = 0
        for user in parents:
            if user.parent_to:
                child_name = user.parent_to.username
                content = f'Hello {user.username}, please check your child {child_name}\'s progress updates.'
                Message.objects.create(
                    sender=request.user,
                    recipient=user,
                    content=content
                )
                messages_sent += 1
        
        if messages_sent > 0:
            messages.success(request, f"Message sent to {messages_sent} parent(s).")
        else:
            messages.warning(request, "No eligible parents selected or no children associated with selected parents.")

    send_message_to_parent.short_description = "Send message to selected parents"
    actions = [send_message_to_parent]

admin.site.register(User, UserAdmin)
admin.site.register(Message)
admin.site.register(ProgressUpdate)
admin.site.register(Meeting)