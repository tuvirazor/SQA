# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-15 07:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0022_internshipchoice_internship_choice'),
    ]

    operations = [
        migrations.AddField(
            model_name='internshipoffer',
            name='master',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]