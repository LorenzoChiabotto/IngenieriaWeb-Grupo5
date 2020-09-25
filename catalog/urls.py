
from django.urls import path
from catalog import views
from django.contrib import admin


urlpatterns = [
    path('',views.home, name='home'),
    path('admin/', admin.site.urls),
    path('login/',views.login, name='login'),
    path('signup/',views.signup, name='signup'),
    path('logout/',views.logout, name='logout'),
    path('waitingConfirmation/', views.waitingConfirmation, name='waitingConfirmation'),
    path('chat_rooms/',views.chat_rooms, name='chat_rooms'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('myProfile/', views.myProfile, name='myProfile'),
    path('chat_rooms/create', views.create_chat_room, name='create_chat_room'),
    #path('chat_rooms/chat/<chat_pk>', views.chat,  name='chat'),
    path('profile/<user_pk>', views.profile,  name='profile'),


]
