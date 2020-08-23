
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
]
