# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-11 20:37
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match_accounts', '0024_rename_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteprofile',
            name='marital_status',
            field=models.SmallIntegerField(choices=[(0, 'Unknown'), (1, 'Single'), (2, 'Divorced'), (3, 'Widowed'), (4, 'In a relatioship'), (5, 'In an open relationship'), (6, "It's complicated"), (7, 'Separated'), (8, 'Married')], default=0, verbose_name='marital status'),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='smoking_status',
            field=models.SmallIntegerField(choices=[(0, 'Unknown'), (1, 'No'), (2, 'Sometimes'), (3, 'Yes')], default=0, verbose_name='smoking status'),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='smoking_status_match',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=None, verbose_name='smoking status match'),
        ),
    ]
