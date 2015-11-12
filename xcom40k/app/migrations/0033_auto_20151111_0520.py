# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_auto_20151111_0513'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ItemMarket',
            new_name='ItemMarketToken',
        ),
    ]
