# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-26 16:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dissertation', '0008_dissertation_defend_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dissertationrole',
            name='status',
            field=models.CharField(choices=[('PROMOTEUR', 'pro'), ('CO_PROMOTEUR', 'copro'), ('READER', 'reader')], max_length=12),
        ),
    ]
