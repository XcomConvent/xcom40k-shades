# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_auto_20151017_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='participants',
            field=models.ManyToManyField(to='app.Char', blank=True),
        ),
    ]
