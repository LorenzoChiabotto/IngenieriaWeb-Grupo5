from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class MotivosDenuncias(models.Model):
    name = models.CharField(max_length=30)
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



