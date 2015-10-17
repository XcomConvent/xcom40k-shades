# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_auto_20151017_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='finalize_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
