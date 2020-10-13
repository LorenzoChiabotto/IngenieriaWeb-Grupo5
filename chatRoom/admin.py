from django.contrib import admin

from .models import Message, Kicked_out_user, Chatroom,Report, Type_Report


admin.site.register(Message)
admin.site.register(Kicked_out_user)
admin.site.register(Chatroom)
admin.site.register(Report)
admin.site.register(Type_Report)