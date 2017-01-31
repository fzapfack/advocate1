# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-24 10:55
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('listener', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='lang',
            field=models.CharField(db_tablespace='indexes', default='FR', max_length=10),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='place',
            field=models.CharField(db_tablespace='indexes', default='NULL', max_length=30),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='replied_to',
            field=models.IntegerField(db_tablespace='indexes', default=-1),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='sentiment',
            field=models.IntegerField(choices=[(1, 'Positif'), (-1, 'Negatif'), (0, 'Neutre'), (2, 'Inconnu')], db_tablespace='indexes', default=2),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='topic',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('GE', 'General'), ('EC', 'Economie'), ('SA', 'Sante'), ('PS', 'Parti Socialiste'), ('LR', 'Les Republicains'), ('FN', 'Front National'), ('EM', 'En Marche')], max_length=20),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='txt',
            field=models.CharField(db_tablespace='indexes', max_length=200),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='usr_twitter_id',
            field=models.IntegerField(db_tablespace='indexes'),
        ),
    ]
