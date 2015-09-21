# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_ability_cls'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Class',
        ),
    ]
