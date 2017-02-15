from django.db import models

# Create your models here.

import datetime
from django.utils import timezone


class Teste(models.Model):
   teste_text = models.CharField(max_length=200)

   def __str__(self):
       return self.teste_text