# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0013_auto_20120104_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='char',
            name='host',
            field=models.ForeignKey(default=2, to=settings.AUTH_USER_MODEL),
        ),
    ]
