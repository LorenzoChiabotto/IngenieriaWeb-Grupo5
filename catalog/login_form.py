from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import (
    authenticate,get_user_model)
User = get_user_model()
class CustomUserForm(UserCreationForm):

    pass

class SignUpForm(UserCreationForm):
        class Meta:
            model = User
            fields = ('email', 'first_name', 'last_name', 'username')