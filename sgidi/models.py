from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from django.contrib.auth.models import User


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
    # AVALIACAO
    total = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    autor_pre_analise = models.ForeignKey(User, null=True, related_name="avaliador1")
    data_pre_analise = models.DateTimeField(null=True)
    pre_analise = models.TextField(max_length=1700)
    autor_analise = models.ForeignKey(User, null=True, related_name="avaliador2")
    data_analise = models.DateTimeField(null=True)
    analise = models.TextField(max_length=1700)

    def __str__(self):
        return self.nome


class Analises(models.Model):
    ideia = models.ForeignKey(Ideias, unique=False, related_name='avaliacaoes')
    ordem = models.IntegerField(validators=[MaxValueValidator(14), MinValueValidator(0)])
    avaliacao = models.CharField(max_length=110, null=True)
    tipo = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)], null=True)
    peso = models.IntegerField(validators=[MaxValueValidator(99), MinValueValidator(0)])

    def __str__(self):
        return self.avaliacao


class AnalisesDefault(models.Model):
    avaliacao = models.CharField(max_length=110, null=True)
    peso = models.IntegerField(validators=[MaxValueValidator(99), MinValueValidator(0)])

    def __str__(self):
        return self.avaliacao


class Tokens(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=50)

    def __str__(self):
        return self.token


class Tags(models.Model):
    tag = models.CharField(max_length=110, null=False)
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.tag


class Conhecimentos(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=110, null=True)
    texto = models.TextField(max_length=1700)
    data = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tags)

    def __str__(self):
        return self.titulo


class Notificacoes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    conhecimento = models.ForeignKey(Conhecimentos,on_delete=models.CASCADE)

    def __str__(self):
        return self.read
