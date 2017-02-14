# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-13 08:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0014_auto_20170212_0231'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='color_pred',
            field=models.CharField(default='GREY', max_length=20),
        ),
        migrations.AddField(
            model_name='region',
            name='num_tweets_neg_pred',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='region',
            name='num_tweets_net_pred',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='region',
            name='num_tweets_pos_pred',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='region',
            name='color',
            field=models.CharField(default='GREY', max_length=20),
        ),
        migrations.AlterField(
            model_name='region',
            name='num_tweets_neg',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='region',
            name='num_tweets_net',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='region',
            name='num_tweets_pos',
            field=models.IntegerField(default=0),
        ),
    ]