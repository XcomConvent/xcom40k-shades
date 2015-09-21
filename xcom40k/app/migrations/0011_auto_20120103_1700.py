# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_ability_cls'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemtoken',
            name='desc',
        ),
        migrations.RemoveField(
            model_name='itemtoken',
            name='name',
        ),
    ]
