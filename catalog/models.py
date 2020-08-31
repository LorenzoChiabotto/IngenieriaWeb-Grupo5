from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class User_validable(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
    token = models.CharField(max_length=255)    
    followed_tags = models.ManyToManyField(Tag,  related_name="User_tags")
    
    def __str__(self):
        return self.user.username

class Message(models.Model):
    user = models.OneToOneField(User, on_delete=models.NOT_PROVIDED)
    message = models.CharField(max_length=255)
    time = models.TimeField()

class Kicked_out_user(models.Model):
    user = models.OneToOneField(User, on_delete=models.NOT_PROVIDED)
    time = models.TimeField()
    def __str__(self):
        return self.user.username

class Chatroom(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
    administrator = models.OneToOneField(User_validable, on_delete=models.NOT_PROVIDED)
    moderators = models.ManyToManyField(User_validable,  related_name="Chat_moderators")
    tags = models.ManyToManyField(Tag,  related_name="Chatroom_tags")
    users = models.ManyToManyField(User_validable,  related_name="Chat_users")
    banned_users = models.ManyToManyField(User_validable,  related_name="Chat_banned")
    kicked_out_user = models.ManyToManyField(Kicked_out_user,  related_name="Chat_kickeds")
    messages = models.ManyToManyField(Message,  related_name="Chat_messages")
    messages_per_minute = models.IntegerField()
    time_between_messages = models.TimeField()
    max_users = models.IntegerField()
    duration = models.IntegerField()
    def __str__(self):
        return self.name