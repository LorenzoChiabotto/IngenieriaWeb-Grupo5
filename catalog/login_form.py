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
class Userloginform(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    def clan(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username,password=password)
            if not user:
                raise forms.ValidationError('El usuario no existe')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrecto password ')
            if not user.is_active:
                raise forms.ValidationError('Usuario no activo')
        return super(Userloginform,self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email Address')
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = {
            'username'
        }



class SignUpForm(UserCreationForm):
        class Meta:
            model = User
            fields = ('email', 'first_name', 'last_name', 'username')