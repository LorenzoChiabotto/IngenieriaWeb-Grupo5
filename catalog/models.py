from django.db import models
from django.contrib.auth.models import User

class User_validable(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
    token = models.CharField(max_length=255)