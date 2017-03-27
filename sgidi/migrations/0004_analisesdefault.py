# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-23 11:40
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgidi', '0003_auto_20170308_1218'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalisesDefault',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avaliacao', models.CharField(max_length=110, null=True)),
                ('peso', models.IntegerField(validators=[django.core.validators.MaxValueValidator(99), django.core.validators.MinValueValidator(0)])),
            ],
        ),
    ]
