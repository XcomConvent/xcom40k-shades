# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20120103_1617'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameField(
            model_name='char',
            old_name='classes',
            new_name='abilities',
        ),
        migrations.AddField(
            model_name='ability',
            name='cls',
            field=models.OneToOneField(default=None, to='app.Class'),
        ),
    ]
