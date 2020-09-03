from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class User_validable(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
    token = models.CharField(max_length=255, blank=True)    
    followed_tags = models.ManyToManyField(Tag,  related_name="User_tags", blank=True)
    
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
    administrator = models.ManyToManyField(User_validable, related_name="Chat_administrators",)
    moderators = models.ManyToManyField(User_validable,  related_name="Chat_moderators", blank=True)
    tags = models.ManyToManyField(Tag, related_name="Chatroom_tags")
    users = models.ManyToManyField(User_validable,  related_name="Chat_users", blank=True)
    banned_users = models.ManyToManyField(User_validable,  related_name="Chat_banned", blank=True)
    kicked_out_user = models.ManyToManyField(Kicked_out_user,  related_name="Chat_kickeds", blank=True)
    messages = models.ManyToManyField(Message,  related_name="Chat_messages", blank=True)
    messages_per_minute = models.IntegerField()
    time_between_messages = models.IntegerField()
    max_users = models.IntegerField()
    duration = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name

