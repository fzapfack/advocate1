# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-22 16:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listener', '0022_auto_20170309_0832'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='training_tweet',
            field=models.BooleanField(default=False),
        ),
    ]
