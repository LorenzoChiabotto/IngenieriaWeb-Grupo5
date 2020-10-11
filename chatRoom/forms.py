from django import forms
from django.forms import ModelForm
from .models import Message, Tag, Chatroom,MotivosDenuncias, Denuncias
from django.forms import ModelForm,TextInput, Textarea, ModelChoiceField, SelectMultiple

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



class New_Report(ModelForm):
    motivos = MotivosDenuncias.objects.all()
    class Meta:
        model = Denuncias
        fields = ["motivos"]
        widgets = {
            'motivos' : SelectMultiple(attrs={'class':'form-control'})
        }

    pass
class FormMessage(ModelForm):
    class Meta:
        model = Message
        fields = ["message","image","file", "user", "chatroom"]