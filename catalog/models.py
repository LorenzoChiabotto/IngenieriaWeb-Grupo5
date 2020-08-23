from django.db import models

class Home(models.Model):
    titulo = models.CharField(max_length=50)
    texto = models.CharField(max_length=200)

class Usuario(models.Model):
    usuario = models.CharField(max_length=25)
    mail = models.CharField(max_length=20)
    password1 = models.CharField(max_length=20)
