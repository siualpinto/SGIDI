# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-15 19:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgidi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analises',
            name='ideia',
        ),
        migrations.DeleteModel(
            name='AnalisesDefault',
        ),
        migrations.RemoveField(
            model_name='conhecimentos',
            name='autor',
        ),
        migrations.RemoveField(
            model_name='conhecimentos',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='ideias',
            name='autor',
        ),
        migrations.RemoveField(
            model_name='ideias',
            name='autor_analise',
        ),
        migrations.RemoveField(
            model_name='ideias',
            name='autor_pre_analise',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='user',
        ),
        migrations.RemoveField(
            model_name='tokens',
            name='user',
        ),
        migrations.DeleteModel(
            name='Analises',
        ),
        migrations.DeleteModel(
            name='Conhecimentos',
        ),
        migrations.DeleteModel(
            name='Ideias',
        ),
        migrations.DeleteModel(
            name='Tags',
        ),
        migrations.DeleteModel(
            name='Tokens',
        ),
    ]
