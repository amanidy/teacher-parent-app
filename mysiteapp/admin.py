from django.contrib import admin
from .models import User, Message, ProgressUpdate, Meeting
from django.contrib import messages
from .forms import AdminUserCreationForm  

class UserAdmin(admin.ModelAdmin):
    form = AdminUserCreationForm
    list_display = ['username', 'role', 'parent_to', 'is_staff', 'is_superuser']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'parent_to')
        }),
    )
    
    def send_message_to_parent(self, request, queryset):
        parents = queryset.filter(role='parent')
        messages_sent = 0
        for user in parents:
            if user.parent_to:
                child_name = user.parent_to.username
                content = f'Hello {user.username}, please check your child {child_name}\'s progress updates.'
                Message.objects.create(
                    sender=request.user,
                    receiver=user,
                    content=content
                )
                messages_sent += 1
        
        if messages_sent > 0:
            messages.success(request, f"Message sent to {messages_sent} parent(s).")
        else:
            messages.warning(request, "No eligible parents selected or no children associated with selected parents.")

    send_message_to_parent.short_description = "Send message to selected parents"
    actions = [send_message_to_parent]



class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp','reply_to', 'view_replies')
    list_filter = ('sender', 'receiver', 'timestamp')
    search_fields = ('content', 'sender__username', 'receiver__username')

    def view_replies(self, obj):
        replies = obj.replies.all() 
        if replies.exists():
            return "\n".join([f"Reply from {reply.sender.username}: {reply.content}" for reply in replies])
        return "No replies"
    
    view_replies.short_description = "Replies to this message"

admin.site.register(User, UserAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(ProgressUpdate)
admin.site.register(Meeting)