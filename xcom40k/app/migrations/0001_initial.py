# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ability',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=2000)),
                ('required_level', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AbilityClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('abilities', models.ManyToManyField(to='app.Ability', verbose_name=b'list of abilities')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Char',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=200)),
                ('classes', models.ManyToManyField(to='app.AbilityClass')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=2000)),
                ('slot', models.CharField(max_length=1, choices=[(b's', b'Default Small Slot'), (b'l', b'Default Large Slot')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ItemToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=2000)),
                ('count', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
                ('item', models.ForeignKey(to='app.Item')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='char',
            name='items',
            field=models.ManyToManyField(to='app.ItemToken'),
        ),
    ]
