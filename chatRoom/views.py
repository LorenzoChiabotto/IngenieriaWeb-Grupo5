from django.contrib.auth.models import User, auth
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import Context, Template
from django.template.loader import render_to_string

from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse

from datetime import timedelta
from django.utils import timezone
from catalog.models import User_validable
from .models import Chatroom, Kicked_out_user,Message,Tag
from .forms import FormMessage, New_Chatroom
from django.conf import settings

import json

from django.db.models import Q

def chat_rooms(request):
    userRooms = None
    try:
        request.user = User_validable.objects.get(user=User.objects.get(username=request.user))
        userRooms = list(filter(lambda chatroom: not chatroom.duration or (chatroom.created_at.__add__(timedelta(hours=chatroom.duration)) > timezone.now()), Chatroom.objects.filter(users__user__pk__icontains=User_validable.objects.get(user=User.objects.get(username=request.user)).pk)))
    except:
        pass
    tags = Tag.objects.all()
    queryset = request.GET.get("search")
    querysetTags = request.GET.get("tags")
    
    if queryset is not None:
        rooms =  Chatroom.objects.filter(
            Q(name__icontains = queryset) |
            Q(description__icontains = queryset)
        )
    else:
        rooms = Chatroom.objects.all()
    if querysetTags is not None and querysetTags != '':
        rooms =  rooms.filter(
            tags__pk__icontains=querysetTags
        )

    filteredRooms = list(filter(lambda chatroom: not chatroom.duration or (chatroom.created_at.__add__(timedelta(hours=chatroom.duration)) > timezone.now()), rooms))
    contexto = {'rooms': filteredRooms, 'tags':tags, 'userRooms':userRooms, 'tagsSelected':querysetTags}
    if(userRooms is not None): 
        contexto = {'rooms': filteredRooms, 'tags':tags, 'userRooms':userRooms, 'tagsSelected':querysetTags}
    
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
                duration=duration,
                administrator=User_validable.objects.get(user=(request.user.user)))

            room.save()
            room.tags.set(Tag.objects.filter(id__in=tags))
            room.users.set([request.user])
            room.save()
            return redirect('chatRoom:room',room_pk=room.pk)


    return render(request, 'create_chat_room.html', {'form_new_chatroom': form_new_chatroom})


def room(request, room_pk):
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
        

def reportRoom(request, room_pk,user_pk ):
    try:
        Room = Chatroom.objects.get(pk=room_pk)
        Room.complaints_counter +=1
        Room.save()
    except:
        pass
    return redirect('chatRoom:roomsList')

def render_message(request):
    return render(request,'chatMessage.html', )
    

def render_user_message(request):
    return render(request,'chatUserMessage.html', )


def validate_max_chatrooms(user):
    x=0
    user_chatrooms = Chatroom.objects.filter(administrator=user)
    for chatroom in user_chatrooms:
        if(chatroom.duration is not None):
            if timezone.now() < chatroom.created_at.__add__(timedelta(hours=chatroom.duration)):
                x+=1
            if(x >= 3):
                return False
    return True

def send_message(request):
    if(request.method == 'POST'):
        strType = 'chat_message'
        strMessage = request.POST.get("message")
        strUserPk = request.POST.get("user")

        if(str(strMessage).startswith("/kick ")):
            splitted = str(strMessage).split(" ")
            if(len(splitted) == 2):
                strUserPk = kickUser(request.POST.get("chatroom"), request.POST.get("user"), splitted[1])
                if(strUserPk is None):
                    return JsonResponse({})
                strType = 'kick_message'
                strMessage = splitted[1] + " has been kicked out"
        if(str(strMessage).startswith("/ban ")):
            splitted = str(strMessage).split(" ")
            if(splitted.count != 3):
                if(not kickUser(request.POST.get("chatroom"), request.POST.get("user"), splitted[1]), splitted[2]):
                    return JsonResponse({})
                strType = 'ban_message'
                strMessage = splitted[1] + " has been banned - " + splitted[2]
                
        form_message = FormMessage(request.POST, request.FILES)
        if form_message.is_valid():
            message = form_message.save()
            message.message = strMessage
            message.type = strType
            message.user = strUserPk
            message.save()
            return JsonResponse(
                {
                    'type': strType,
                    'message': strMessage,
                    'userId': message.user.user.pk,
                    'userName': message.user.user.username,
                    'image': settings.MEDIA_URL+str(message.image),
                    'file': settings.MEDIA_URL+str(message.file)
                })
        else:
            return JsonResponse(form_message)



def get_messages(request, room_pk, last_time):
    if(request.method == 'GET'):
        if(last_time != "0"):
            messages = Message.objects.filter(chatroom=room_pk, time__gt=last_time)
        else:
            messages = Message.objects.filter(chatroom=room_pk)

        returnMessages = []
        for message in messages:
            returnMessages.append(
                {
                    'type': message.type,
                    'message': message.message,
                    'userId': message.user.user.pk,
                    'userName': message.user.user.username,
                    'image': settings.MEDIA_URL+str(message.image),
                    'file': settings.MEDIA_URL+str(message.file),
                    'last_time': str(message.time)
                }
            )
        return HttpResponse(json.dumps(returnMessages), content_type="application/json")


def leave(request, room_pk, user_pk):
    try:
        user_off = User_validable.objects.get(pk=user_pk)
        chat = Chatroom.objects.get(pk=room_pk)
        chat.users.remove(user_off)
    except:
        pass
    return redirect('chatRoom:roomsList')


def kickUser(room_pk, user_pk,user_kick):
    try:
        user_off = User_validable.objects.get(user=User.objects.get(username=user_kick))
        user_admin = User_validable.objects.get(pk=user_pk)
        chat = Chatroom.objects.get(pk=room_pk)
        if ((user_admin == chat.administrator)| (user_admin == chat.moderators)):
            chat.users.remove(user_off)
            chat.kicked_out_user.add(Kicked_out_user.objects.create(user = user_off, time=timezone.now()))
        else:
            return None
        return user_off
    except:
        return None
    


"""
user = models.ForeignKey(User_validable, on_delete=models.CASCADE)
    message = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="messages_images", blank=True)
    file = models.FileField(upload_to="messages_files", blank=True)
    time = models.TimeField(default=now)
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE)"""