# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20150922_1509'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassLevelPair',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.PositiveIntegerField(default=0)),
                ('cls', models.ForeignKey(to='app.Class')),
            ],
        ),
        migrations.AlterField(
            model_name='neurorequest',
            name='closed_date',
            field=models.DateField(default=datetime.datetime(2015, 9, 22, 17, 50, 52, 826350, tzinfo=utc)),
        ),
    ]
