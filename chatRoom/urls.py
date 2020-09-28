from django.urls import path

from . import views

app_name = 'chatRoom'
urlpatterns = [
    path('render_message', views.render_message,  name='render_message'),
    path('render_user_message', views.render_user_message,  name='render_user_message'),
    path('send_message', views.send_message,  name='send_message'),
    path('get_messages/<str:room_pk>/<str:last_time>', views.get_messages,  name='get_messages'),

    path('rooms/list',views.chat_rooms, name='roomsList'),
    path('rooms/create', views.create_chat_room, name='roomsCreate'),
    path('rooms/<str:room_pk>', views.room,  name='room'),
    
    path('rooms/kickUser/<room_pk>/<user_pk>/<user_kick>', views.kickUser,  name='kickUser'),

]

