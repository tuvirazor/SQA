# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-15 14:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dissertation', '0008_dissertation_defend_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dissertation',
            name='defend_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.AcademicYear'),
        ),
    ]
