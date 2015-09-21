# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20120103_1632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ability',
            name='cls',
        ),
    ]
