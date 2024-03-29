# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-15 19:07
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Analises',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordem', models.IntegerField(validators=[django.core.validators.MaxValueValidator(14), django.core.validators.MinValueValidator(0)])),
                ('avaliacao', models.CharField(max_length=110, null=True)),
                ('tipo', models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('peso', models.IntegerField(validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='AnalisesDefault',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avaliacao', models.CharField(max_length=110, null=True)),
                ('peso', models.IntegerField(validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='Conhecimentos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=110, null=True)),
                ('texto', models.TextField(max_length=1700)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ideias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=110)),
                ('tipo', models.IntegerField(validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(0)])),
                ('tipo_nome', models.CharField(max_length=110)),
                ('estado', models.IntegerField(validators=[django.core.validators.MaxValueValidator(3), django.core.validators.MinValueValidator(0)])),
                ('estado_nome', models.CharField(max_length=20)),
                ('problema', models.TextField(max_length=1700)),
                ('solucao', models.TextField(max_length=1700)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=3, max_digits=5, null=True)),
                ('data_pre_analise', models.DateTimeField(null=True)),
                ('pre_analise', models.TextField(max_length=1700)),
                ('data_analise', models.DateTimeField(null=True)),
                ('analise', models.TextField(max_length=1700)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('autor_analise', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='avaliador2', to=settings.AUTH_USER_MODEL)),
                ('autor_pre_analise', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='avaliador1', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=110)),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tokens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='conhecimentos',
            name='tag',
            field=models.ManyToManyField(to='sgidi.Tags'),
        ),
        migrations.AddField(
            model_name='analises',
            name='ideia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avaliacaoes', to='sgidi.Ideias'),
        ),
    ]
