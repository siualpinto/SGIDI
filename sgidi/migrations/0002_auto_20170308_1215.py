# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-08 12:15
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgidi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analises',
            name='ordem',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(15), django.core.validators.MinValueValidator(1)]),
        ),
    ]
