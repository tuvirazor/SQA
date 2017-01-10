# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-01 22:55
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0038_auto_20160502_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagetemplate',
            name='language',
            field=models.CharField(choices=[('fr-be', 'French'), ('en', 'English')], default='fr-be', max_length=30),
        ),
        migrations.AlterField(
            model_name='messagetemplate',
            name='reference',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='messagetemplate',
            name='template',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterUniqueTogether(
            name='messagetemplate',
            unique_together=set([('reference', 'language')]),
        ),
    ]