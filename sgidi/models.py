from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from decimal import Decimal

# Create your models here.

class Ideias(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=110)
    tipo = models.IntegerField(validators=[MaxValueValidator(5)])
    tipo_nome = models.CharField(max_length=110)
    estado = models.IntegerField(validators=[MaxValueValidator(4)])
    estado_nome = models.CharField(max_length=20)
    problema = models.TextField(max_length=1700)
    solucao = models.TextField(max_length=1700)
    data = models.DateTimeField(auto_now_add=True)
    #AVALIACAO
    total = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    autor_pre_analise = models.ForeignKey(User, null=True, related_name="avaliador1")
    data_pre_analise = models.DateTimeField(null=True)
    pre_analise = models.TextField(max_length=1700)
    autor_analise = models.ForeignKey(User, null=True, related_name="avaliador2")
    data_analise = models.DateTimeField(null=True)
    analise = models.TextField(max_length=1700)

    def __str__(self):
        return self.nome

class Analise(models.Model):
    ideia = models.ForeignKey(Ideias, unique=False, related_name='avaliacaoes')
    ordem = models.IntegerField(validators=[MaxValueValidator(15)])
    avaliacao = models.CharField(max_length=110, null=True)
    tipo = models.IntegerField(validators=[MaxValueValidator(5)], null=True)
    peso = models.DecimalField(max_digits=5, decimal_places=3)

    def __str__(self):
        return self.avaliacao




