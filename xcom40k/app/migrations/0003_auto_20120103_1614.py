# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20120103_1604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abilityset',
            name='abilities',
        ),
        migrations.AddField(
            model_name='ability',
            name='exp_cost',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='char',
            name='classes',
            field=models.ManyToManyField(to='app.Ability'),
        ),
        migrations.DeleteModel(
            name='AbilitySet',
        ),
    ]
