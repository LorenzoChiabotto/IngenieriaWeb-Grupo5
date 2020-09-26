from django.contrib.auth.models import User, auth
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import Context, Template
from django.template.loader import render_to_string

from django.shortcuts import render,redirect
from django.http import HttpResponse



from datetime import timedelta
from django.utils import timezone
from catalog.models import User_validable
from .models import Chatroom, Kicked_out_user,Message,Tag
from .forms import FormMessage, New_Chatroom


def chat_rooms(request):
    try:
        request.user = User_validable.objects.get(user=User.objects.get(username=request.user))
    except:
        pass
    rooms = list(filter(lambda chatroom: not chatroom.duration or (chatroom.created_at.__add__(timedelta(hours=chatroom.duration)) > timezone.now())  , Chatroom.objects.all()))
    contexto = {'rooms': rooms}
    return render(request,'chat_rooms.html',contexto)
    
@login_required(login_url='/login/')
def create_chat_room(request):
    try:
        request.user = User_validable.objects.get(user=User.objects.get(username=request.user))
    except:
        pass
    form_new_chatroom = New_Chatroom()
    if request.method == 'POST':
        form_new_chatroom = New_Chatroom(request.POST)
        if form_new_chatroom.is_valid() and validate_max_chatrooms(request.user):
            name = form_new_chatroom.cleaned_data['name']
            description = form_new_chatroom.cleaned_data['description']
            tags = form_new_chatroom.cleaned_data['tags']
            messages_per_minute = form_new_chatroom.cleaned_data['messages_per_minute']
            time_between_messages = form_new_chatroom.cleaned_data['time_between_messages']
            max_users = form_new_chatroom.cleaned_data['max_users']
            duration = form_new_chatroom.cleaned_data['duration']
            room = Chatroom.objects.create(
                name=name,
                description=description,
                messages_per_minute = messages_per_minute,
                time_between_messages = time_between_messages,
                max_users=max_users,
                duration=duration)

            room.administrator.set(User_validable.objects.filter(user=(request.user.user)))
            room.save()
            room.tags.set(Tag.objects.filter(id__in=tags))
            room.users.set([request.user])
            room.save()
            return redirect('chatRoom:roomsList',room_pk=room.pk)


    return render(request, 'create_chat_room.html', {'form_new_chatroom': form_new_chatroom})


def room(request, room_pk):
    print(room_pk)
    chat = Chatroom.objects.get(pk=room_pk)
    form_send_message = FormMessage()
    if chat is not None:
        try:
            request.user = User_validable.objects.get(user=User.objects.get(username=request.user))
            
            chat.users.add(request.user)
        except:
            pass

        return render(request,'room.html', {"chat": chat, 'form_send_message':form_send_message, 'room':room_pk})
    else:
        return render(None, '')
        

def render_message(request):
    return render(request,'chatMessage.html', )
    

def render_user_message(request):
    return render(request,'chatUserMessage.html', )


def validate_max_chatrooms(user):
    x=0
    user_chatrooms = Chatroom.objects.filter(administrator=user)
    for chatroom in user_chatrooms:
        if chatroom.created_at < timezone.now().__add__(timedelta(hours=chatroom.duration)):
            x+=1
        if(x >= 3):
            return False
    return True

def send_message(request):
    if(request.method == 'POST'):
        form_message = FormMessage(request.POST, request.FILES)
        if form_message.is_valid():
            message = form_message.save()
            
            chat = Chatroom.objects.get(pk=request.POST.get('room'))
            chat.messages.add(message)
            return HttpResponse(form_message)
        else:
            return HttpResponse(form_message)