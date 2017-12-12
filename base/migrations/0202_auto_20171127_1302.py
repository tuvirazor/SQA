# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-27 12:02
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0201_auto_20171204_1659'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entitycomponentyear',
            name='deleted',
        ),
        migrations.AddField(
            model_name='entity',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='entitycomponentyear',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='entitycontaineryear',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='entityversion',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, null=True),
        ),
    ]
