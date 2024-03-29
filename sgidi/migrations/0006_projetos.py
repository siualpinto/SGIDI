# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-22 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgidi', '0005_auto_20170521_0006'),
    ]

    operations = [
        migrations.CreateModel(
            name='Projetos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_asana', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('notes', models.TextField(max_length=1700)),
                ('current_status', models.CharField(choices=[('0', 'green'), ('1', 'yellow'), ('2', 'red')], default='0', max_length=1)),
                ('current_status_text', models.TextField(max_length=1700)),
                ('due_date', models.DateTimeField()),
                ('created_at', models.DateTimeField()),
                ('modified_at', models.DateTimeField()),
            ],
        ),
    ]
