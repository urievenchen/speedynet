# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-29 17:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match_accounts', '0008_auto_20170329_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteprofile',
            name='match_description_en',
            field=models.TextField(null=True, verbose_name=''),
        ),
        migrations.AddField(
            model_name='siteprofile',
            name='match_description_he',
            field=models.TextField(null=True, verbose_name=''),
        ),
    ]
