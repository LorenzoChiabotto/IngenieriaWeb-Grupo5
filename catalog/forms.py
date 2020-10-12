from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth import authenticate
from datetime import date

class SignUp(forms.Form):
    user = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(min_length=8,max_length=20,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirm_password = forms.CharField(min_length=8,max_length=20,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def clean_password(self):
        password = self.cleaned_data['password']
        if(len(password) < 8 or not password.isalnum() or password.isnumeric() or password.isalpha()):
            raise ValidationError(
                ["The password should be 8 characters at least.",
                "The password should be alphanumerical."])
        return password

    def clean_confirm_password(self):
        try:
            confirm_password = self.cleaned_data['confirm_password']
            password = self.cleaned_data['password']
            if password == confirm_password:
                return confirm_password
        except:
            pass    
        raise ValidationError(["Passwords didnt match"])

    def clean_user(self):
        user = self.cleaned_data['user']
        if User.objects.filter(username=user).exists():
            raise ValidationError("This user already exist.")
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email already exists")
        
        return email
    def clean_captcha(self):
        return self.cleaned_data['captcha']


class Login(forms.Form):
    user = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean_user(self):
        user = self.cleaned_data['user']
        if not User.objects.filter(username=user).exists():
            raise ValidationError("This user does not exist.")
        return user

    def clean_password(self):
        password = self.cleaned_data['password']
        try:
            username = self.cleaned_data['user']
        except:
            return password
        
        if(username is not None):
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError("Incorrect password.")
            print(user.password)
            return password
        return password


