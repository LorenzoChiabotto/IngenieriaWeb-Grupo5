from django.urls import path

from . import views

app_name = 'chatRoom'
urlpatterns = [
    path('render_message', views.render_message,  name='render_message'),
    path('render_user_message', views.render_user_message,  name='render_user_message'),
    path('rooms/list',views.chat_rooms, name='roomsList'),
    path('rooms/create', views.create_chat_room, name='roomsCreate'),
    path('rooms/<str:room_pk>', views.room,  name='room'),

]

