
from django.urls import path
from catalog import views

app_name="catalog"
urlpatterns = [
    path('',views.home, name='home'),
    path('login/',views.login, name='login'),
    path('signup/',views.signup, name='signup'),
    path('logout/',views.logout, name='logout'),
    path('waitingConfirmation/', views.waitingConfirmation, name='waitingConfirmation'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('myProfile/', views.myProfile, name='myProfile'),
    path('profile/<user_pk>', views.profile,  name='profile'),


]
