# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_auto_20151017_1603'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ability',
            unique_together=set([('name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='char',
            unique_together=set([('name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='class',
            unique_together=set([('name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([('name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='mission',
            unique_together=set([('name',)]),
        ),
    ]
