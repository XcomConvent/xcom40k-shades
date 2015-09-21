# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('pub_date', models.DateField()),
                ('status', models.CharField(max_length=1, choices=[(0, b'Not opened'), (1, b'Opened'), (2, b'Closed'), (3, b'Finalized')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameModel(
            old_name='AbilityClass',
            new_name='AbilitySet',
        ),
        migrations.RemoveField(
            model_name='char',
            name='desc',
        ),
        migrations.AddField(
            model_name='mission',
            name='participants',
            field=models.ManyToManyField(to='app.Char'),
        ),
    ]
