# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 17:09
from __future__ import unicode_literals

from django.db import migrations, models
import speedy.core.accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20170117_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='access_dob_day_month',
            field=speedy.core.accounts.models.UserAccessField(choices=[(1, 'Only me'), (2, 'Me and my friends'), (4, 'Anyone')], default=1, verbose_name='who can view my birth month and day'),
        ),
        migrations.AddField(
            model_name='user',
            name='access_dob_year',
            field=speedy.core.accounts.models.UserAccessField(choices=[(1, 'Only me'), (2, 'Me and my friends'), (4, 'Anyone')], default=1, verbose_name='who can view my birth year'),
        ),
        migrations.AddField(
            model_name='user',
            name='notify_on_message',
            field=models.PositiveIntegerField(choices=[(1, 'Notify me'), (0, "Don't notify me")], default=1, verbose_name='on new messages'),
        ),
    ]
