# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-01 01:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tb_app', '0007_auto_20180225_1526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='trip',
        ),
        migrations.AddField(
            model_name='tripschedule',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='tb_app.User'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Trip',
        ),
    ]
