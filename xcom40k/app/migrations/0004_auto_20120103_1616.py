# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20120103_1614'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mission',
            name='status',
        ),
        migrations.AlterField(
            model_name='ability',
            name='desc',
            field=models.CharField(default=b'', max_length=2000),
        ),
        migrations.AlterField(
            model_name='item',
            name='desc',
            field=models.CharField(default=b'', max_length=2000),
        ),
        migrations.AlterField(
            model_name='itemtoken',
            name='desc',
            field=models.CharField(default=b'', max_length=2000),
        ),
        migrations.AlterField(
            model_name='mission',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2012, 1, 3, 16, 16, 36, 3099, tzinfo=utc)),
        ),
    ]
