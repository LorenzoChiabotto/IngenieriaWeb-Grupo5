from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignUp(forms.Form):
    user = forms.CharField(max_length=20)
    email = forms.EmailField(required=True)
    password = forms.CharField(min_length=8,max_length=20,widget=forms.PasswordInput)
    confirm_password = forms.CharField(min_length=8,max_length=20,widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        user = self.cleaned_data['user']
        email = self.cleaned_data['email']
        if password != confirm_password:
            raise ValidationError("Las contraseñas no coinciden")
        if User.objects.filter(username=user).exists():
            raise ValidationError("Usuario ya existente")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Mail ya existente")
        return password



class Login(forms.Form):
    user = forms.CharField(max_length=50)
    password = forms.CharField(max_length=20,widget=forms.PasswordInput)