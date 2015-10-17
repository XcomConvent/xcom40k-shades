# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_auto_20151008_2102'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogentry',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AlterField(
            model_name='blogentry',
            name='pub_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='blogentry',
            name='text',
            field=models.TextField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='mission',
            name='finalize_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='mission',
            name='pub_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='neurorequest',
            name='closed_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='neurorequest',
            name='pub_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='report',
            name='pub_date',
            field=models.DateTimeField(),
        ),
    ]
