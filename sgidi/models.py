from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

# Create your models here.

import datetime
from django.utils import timezone


class Teste(models.Model):
    teste_text = models.CharField(max_length=200)

    def __str__(self):
        return self.teste_text



class Ideias(models.Model):
    autor = models.ForeignKey(User)
    nome = models.CharField(max_length=110)
    tipo = models.IntegerField(validators=[MaxValueValidator(5)])
    tipo_nome = models.CharField(max_length=110)
    problema = models.TextField(max_length=1700)
    solucao = models.TextField(max_length=1700)
    data = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.nome