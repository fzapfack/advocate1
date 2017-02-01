# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-24 13:52
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('listener', '0004_auto_20170124_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='sentiment_predicted',
            field=models.IntegerField(choices=[(1, 'Positif'), (-1, 'Negatif'), (0, 'Neutre'), (2, 'Inconnu')], db_tablespace='indexes', null=True),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='topic_predicted',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(0, 'General'), (1, 'Economie'), (2, 'Sante'), (3, 'Parti Socialiste'), (4, 'Les Republicains'), (5, 'Front National'), (6, 'En Marche')], max_length=13, null=True),
        ),
    ]