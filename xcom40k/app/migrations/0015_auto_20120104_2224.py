# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_char_host'),
    ]

    operations = [
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='itemtoken',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='itemtoken',
            name='count',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='itemtoken',
            name='price',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='system',
            name='stash',
            field=models.ManyToManyField(to='app.ItemToken'),
        ),
    ]
