# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-22 19:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listener', '0023_tweet_training_tweet'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='training_tweet2',
            field=models.BooleanField(default=False),
        ),
    ]
