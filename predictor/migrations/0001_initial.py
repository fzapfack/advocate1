# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-26 20:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('number_labels', models.IntegerField(default=0)),
                ('number_labels_correct', models.IntegerField(default=0)),
                ('number_labels_incorrect', models.IntegerField(default=0)),
                ('user_email', models.EmailField(max_length=254, null=True)),
            ],
        ),
    ]
