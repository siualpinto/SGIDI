from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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
    autor_pre_analise = models.ForeignKey(User, null=True, related_name="avaliador1", on_delete=models.CASCADE)
    data_pre_analise = models.DateTimeField(null=True)
    pre_analise = models.TextField(max_length=1700)
    autor_analise = models.ForeignKey(User, null=True, related_name="avaliador2", on_delete=models.CASCADE)
    data_analise = models.DateTimeField(null=True)
    analise = models.TextField(max_length=1700)

    def __str__(self):
        return self.nome


class Analises(models.Model):
    ideia = models.ForeignKey(Ideias, unique=False, related_name='avaliacaoes', on_delete=models.CASCADE)
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


class Projetos(models.Model):
    STATUS_CHOICES = (
        ('0', 'green'),
        ('1', 'yellow'),
        ('2', 'red'),
    )
    id_asana = models.CharField(max_length=20, null=False)
    name = models.CharField(max_length=100, null=False)
    notes = models.TextField(max_length=1700)
    current_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    current_status_text = models.TextField(max_length=1700)
    due_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(null=True)
    modified_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


class Tasks(models.Model):
    id_asana = models.CharField(max_length=20, null=False)
    name = models.CharField(max_length=100, null=False)
    notes = models.TextField(max_length=1700)
    assignee = models.CharField(max_length=100, null=True)
    assignee_status = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True)
    due_on = models.DateField(null=True)
    due_at = models.DateTimeField(null=True)
    modified_at = models.DateTimeField(null=True)
    section = models.BooleanField(default=False)
    section_id = models.CharField(max_length=20, null=False)
    projeto_id = models.CharField(max_length=20, null=False)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Objetivos(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    text = models.CharField(max_length=2000, null=True)

    def __str__(self):
        return self.text


class NaoConformidades(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    text = models.CharField(max_length=2000, null=True)

    def __str__(self):
        return self.text
