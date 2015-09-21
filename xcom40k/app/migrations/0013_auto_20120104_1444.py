# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_report'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='author',
            new_name='related_char',
        ),
    ]
