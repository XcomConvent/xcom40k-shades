# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_auto_20120106_2212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogentry',
            name='tags',
        ),
        migrations.DeleteModel(
            name='BlogEntryTag',
        ),
    ]
