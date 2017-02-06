# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-06 00:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listener', '0014_auto_20170202_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='retweet_twitter_id',
            field=models.CharField(db_tablespace='indexes', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='tweet',
            name='twitter_id',
            field=models.CharField(db_tablespace='indexes', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='replied_to',
            field=models.CharField(db_tablespace='indexes', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='usr_twitter_id',
            field=models.CharField(db_tablespace='indexes', max_length=30, null=True),
        ),
    ]
