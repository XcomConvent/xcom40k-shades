# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='ability',
            name='cls',
            field=models.ForeignKey(default=None, to='app.Class'),
        ),
    ]
