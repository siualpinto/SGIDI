# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-22 15:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgidi', '0006_projetos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projetos',
            name='created_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='projetos',
            name='due_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='projetos',
            name='modified_at',
            field=models.DateTimeField(null=True),
        ),
    ]