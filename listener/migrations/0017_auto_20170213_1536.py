# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-13 15:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listener', '0016_auto_20170213_0833'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tweet',
            old_name='added_carte',
            new_name='added_map',
        ),
        migrations.RenameField(
            model_name='tweet',
            old_name='added_carte_pred',
            new_name='added_map_pred',
        ),
    ]
