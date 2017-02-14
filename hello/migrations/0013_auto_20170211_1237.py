# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-11 12:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0012_auto_20170211_1115'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('region_code', models.IntegerField()),
                ('department_code', models.CharField(max_length=10)),
                ('name', models.CharField(db_index=True, max_length=60)),
                ('geometry', models.TextField(null=True)),
                ('num_tweets_pos', models.IntegerField(null=True)),
                ('num_tweets_neg', models.IntegerField(null=True)),
                ('num_tweets_net', models.IntegerField(null=True)),
                ('color', models.CharField(default='GREY', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Departement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('code', models.CharField(max_length=10)),
                ('region_code', models.IntegerField()),
                ('name', models.CharField(db_index=True, max_length=60)),
                ('geometry', models.TextField(null=True)),
                ('num_tweets_pos', models.IntegerField(null=True)),
                ('num_tweets_neg', models.IntegerField(null=True)),
                ('num_tweets_net', models.IntegerField(null=True)),
                ('color', models.CharField(default='GREY', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('code', models.IntegerField(db_index=True)),
                ('name', models.CharField(max_length=60)),
                ('name2', models.CharField(max_length=60)),
                ('geometry', models.TextField(null=True)),
                ('num_tweets_pos', models.IntegerField(null=True)),
                ('num_tweets_neg', models.IntegerField(null=True)),
                ('num_tweets_net', models.IntegerField(null=True)),
                ('color', models.CharField(default='GREY', max_length=10)),
            ],
        ),
        migrations.DeleteModel(
            name='DepartementFRModel',
        ),
        migrations.DeleteModel(
            name='RegionFRModel',
        ),
        migrations.DeleteModel(
            name='VilleFRModel',
        ),
    ]
