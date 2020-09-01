from django.contrib import admin

from .models import User_validable, Message, Kicked_out_user, Chatroom, Tag

admin.site.register(User_validable)
admin.site.register(Tag)
#admin.site.register(Message)
#admin.site.register(Kicked_out_user)
admin.site.register(Chatroom)