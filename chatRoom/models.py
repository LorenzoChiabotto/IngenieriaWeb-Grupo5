from django.db import models
from catalog.models import User_validable, User, Tag
from django.utils import timezone
from django.utils.timezone import now

class Kicked_out_user(models.Model):
    user = models.ForeignKey(User_validable, on_delete=models.NOT_PROVIDED,)
    time = models.TimeField()
    def __str__(self):
        return self.user.user.username


class Type_Report(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Report(models.Model):
    usuario = models.ForeignKey(User_validable, on_delete=models.NOT_PROVIDED)
    types = models.ManyToManyField('chatRoom.Type_Report', related_name="Reports_Motives")
    description = models.CharField(max_length=255)
    def __str__(self):
        return self.description

class Chatroom(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
    administrator = models.ForeignKey(User_validable, on_delete=models.CASCADE)
    moderators = models.ManyToManyField(User_validable,  related_name="Chat_moderators", blank=True)
    tags = models.ManyToManyField(Tag, related_name="Chatroom_tags")
    users = models.ManyToManyField(User_validable,  related_name="Chat_users", blank=True)
    banned_users = models.ManyToManyField(User_validable,  related_name="Chat_banned", blank=True)
    reports = models.ManyToManyField('chatRoom.Report',  related_name="Chat_reports", blank=True)
    kicked_out_user = models.ManyToManyField(Kicked_out_user,  related_name="Chat_kickeds", blank=True)
    messages_per_minute = models.IntegerField()
    time_between_messages = models.IntegerField()
    max_users = models.IntegerField()
    duration = models.IntegerField(blank=True,null=True)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User_validable, on_delete=models.CASCADE)
    message = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="messages_images", blank=True)
    file = models.FileField(upload_to="messages_files", blank=True)
    time = models.TimeField(default=now)
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, default='chat_message')

    def __str__(self): 
        return str(self.pk) + '-' + self.chatroom.name + '-' + str(self.user.user.pk)