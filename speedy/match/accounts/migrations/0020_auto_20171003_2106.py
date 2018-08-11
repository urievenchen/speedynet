# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-03 21:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import speedy.match.accounts.validators


class Migration(migrations.Migration):

    dependencies = [
        ('match_accounts', '0019_auto_20170728_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteprofile',
            name='smoking',
            field=models.SmallIntegerField(choices=[(1, 'No'), (2, 'Sometimes'), (3, 'Yes')], default=0, validators=[speedy.match.accounts.validators.validate_smoking_status], verbose_name='smoking status'),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='speedy_match_site_profile', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
