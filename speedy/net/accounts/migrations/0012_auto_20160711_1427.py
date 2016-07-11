# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-11 14:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0001_initial'),
        ('accounts', '0011_auto_20160710_1811'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile_picture',
        ),
        migrations.AddField(
            model_name='entity',
            name='photo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='uploads.Image', verbose_name='photo'),
        ),
    ]
