# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_auto_20150924_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='money',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='char',
            name='exp',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
