# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20120104_2224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='system',
            name='stash',
        ),
        migrations.DeleteModel(
            name='System',
        ),
    ]
