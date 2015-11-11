# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_auto_20151017_1632'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemMarket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_token', models.ForeignKey(to='app.ItemToken')),
                ('owner', models.ForeignKey(to='app.Account')),
            ],
        ),
        migrations.AlterField(
            model_name='mission',
            name='participants',
            field=models.ManyToManyField(to='app.Char', blank=True),
        ),
    ]
