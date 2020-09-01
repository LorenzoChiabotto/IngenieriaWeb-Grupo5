from django import forms
from django.forms import ModelForm,TextInput, Textarea, ModelChoiceField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from catalog.models import Chatroom, Tag
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class SignUp(forms.Form):
    user = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(min_length=8,max_length=20,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirm_password = forms.CharField(min_length=8,max_length=20,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

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
    user = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'class':'form-control'}))


class New_Chatroom(ModelForm):
    tags = ModelChoiceField(queryset=Tag.objects.all()),
    class Meta:
        model = Chatroom
        fields = ["name","description","tags","messages_per_minute","time_between_messages", "max_users", "duration"]
        widgets = {
            'name': TextInput(attrs={'class':'form-control'}),
            'description': Textarea(attrs={'class':'form-control'}),
            'messages_per_minute': TextInput(attrs={'class':'form-control'}),
            'time_between_messages': TextInput(attrs={'class':'form-control'}),
            'max_users': TextInput(attrs={'class':'form-control'}),
            'duration': TextInput(attrs={'class':'form-control'}),
        }