# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-11 00:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0005_auto_20170211_0008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='departementfrmodel',
            name='id',
        ),

        migrations.AlterField(
            model_name='departementfrmodel',
            name='code',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='villefrmodel',
            name='code',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
