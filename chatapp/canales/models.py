from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    nombre = models.CharField(max_length=60)

class Mensaje(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    contenido = models.CharField(max_length=300)
    creado = models.DateTimeField(auto_now_add=True)
