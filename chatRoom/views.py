from django.contrib.auth.models import User, auth
from django.shortcuts import render
from catalog.models import User_validable, Tag, Chatroom
from django.template import Context, Template

def room(request, room_pk):
    chat = Chatroom.objects.get(pk=room_pk)
    if chat is not None:
        try:
            request.user = User_validable.objects.get(user=User.objects.get(username=request.user))
            
            chat.users.add(request.user)
        except:
            pass

        return render(request,'room.html', {"chat": chat})
    else:
        return render(None, '')
        

def render_message(request):
    return render(request,'chatMessage.html', )
    

def render_user_message(request):
    return render(request,'chatUserMessage.html', )