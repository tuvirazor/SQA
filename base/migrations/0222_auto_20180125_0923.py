# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-25 08:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0221_auto_20180123_1541'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='learningcontaineryear',
            unique_together=set([('learning_container', 'academic_year')]),
        ),
    ]
