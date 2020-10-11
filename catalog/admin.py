from django.contrib import admin

from .models import User_validable
from chatRoom.models import Message, Kicked_out_user, Chatroom, Tag, Denuncias, MotivosDenuncias

admin.site.register(User_validable)
admin.site.register(Tag)
admin.site.register(Message)
admin.site.register(Kicked_out_user)
admin.site.register(Chatroom)
admin.site.register(Denuncias)
admin.site.register(MotivosDenuncias)