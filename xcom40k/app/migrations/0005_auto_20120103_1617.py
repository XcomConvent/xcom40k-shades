# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20120103_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='pub_date',
            field=models.DateField(),
        ),
    ]
