# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-31 17:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listener', '0007_auto_20170130_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='usr_place',
            field=models.CharField(db_tablespace='indexes', max_length=30, null=True),
        ),
    ]
