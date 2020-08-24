from django import forms
from django.core.exceptions import ValidationError

class SignUp(forms.Form):
    user = forms.CharField(max_length=20)
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=20,widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=20,widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise ValidationError("Las contraseñas no coinciden")

        return password

class Login(forms.Form):
    user = forms.CharField(max_length=50)
    password = forms.CharField(max_length=20,widget=forms.PasswordInput)