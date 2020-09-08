from django import forms
from django.forms import ModelForm,TextInput, Textarea, ModelChoiceField, SelectMultiple
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from catalog.models import Chatroom, Tag
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
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


class New_Chatroom(ModelForm):
    tags = forms.ModelChoiceField(queryset=Tag.objects.all()),
    class Meta:
        model = Chatroom
        fields = ["name","description","tags","messages_per_minute","time_between_messages", "max_users", "duration"]
        widgets = {
            'name': TextInput(attrs={'class':'form-control'}),
            'description': Textarea(attrs={'class':'form-control'}),
            'messages_per_minute': TextInput(attrs={'class':'form-control', 'type':'number', 'min':'0'}),
            'time_between_messages': TextInput(attrs={'class':'form-control', 'type':'number', 'min':'0'},),
            'max_users': TextInput(attrs={'class':'form-control', 'type':'number', 'min':'1'}),
            'duration': TextInput(attrs={'class':'form-control', 'type':'number', 'required':''}),
            'tags' : SelectMultiple(attrs={'class':'form-control'})
        }

    
    def clean_duration(self):
        duration = self.cleaned_data['duration']
        if(not duration):
            raise ValidationError("Duration is a required field")
        return duration          
    