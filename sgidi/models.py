from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Ideias(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=110)
    tipo = models.IntegerField(validators=[MaxValueValidator(4), MinValueValidator(0)])
    tipo_nome = models.CharField(max_length=110)
    estado = models.IntegerField(validators=[MaxValueValidator(3), MinValueValidator(0)])
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
# TODO iNSERIR MinValueValidator NOS INTEIROS QUE FALTAM
class Analises(models.Model):
    ideia = models.ForeignKey(Ideias, unique=False, related_name='avaliacaoes')
    ordem = models.IntegerField(validators=[MaxValueValidator(14), MinValueValidator(0)])
    avaliacao = models.CharField(max_length=110, null=True)
    tipo = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)], null=True)
    peso = models.IntegerField(validators=[MaxValueValidator(99), MinValueValidator(0)])

    def __str__(self):
        return self.avaliacao




