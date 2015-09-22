# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20150922_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemtoken',
            name='count',
            field=models.PositiveIntegerField(),
        ),
    ]
