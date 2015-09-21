# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20120103_1700'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=10000)),
                ('pub_date', models.DateField()),
                ('author', models.ForeignKey(to='app.Char')),
                ('related_mission', models.ForeignKey(to='app.Mission')),
            ],
        ),
    ]
