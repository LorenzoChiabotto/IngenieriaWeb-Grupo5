from django.contrib import admin

from .models import User_validable, Tag

admin.site.register(User_validable)
admin.site.register(Tag)