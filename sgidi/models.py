from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

# Create your models here.



class Analise(models.Model):
    avaliacao = models.CharField(max_length=110)
    tipo = models.IntegerField(validators=[MaxValueValidator(5)])
    peso = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.avaliacao

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
    autor_pre_analise = models.ForeignKey(User, null=True, related_name="avaliador1")
    data_pre_analise = models.DateTimeField(auto_now=True)
    pre_analise = models.TextField(max_length=1700)
    autor_analise = models.ForeignKey(User, null=True, related_name="avaliador2")
    data_analise = models.DateTimeField(auto_now=True)
    tabela_analise = models.ForeignKey(Analise, null=True)
    analise = models.TextField(max_length=1700)

    def __str__(self):
        return self.nome





