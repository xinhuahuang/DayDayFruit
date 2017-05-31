# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uname', models.CharField(max_length=20)),
                ('pword', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.CharField(default=b'', max_length=20)),
                ('address', models.CharField(default=b'', max_length=100)),
                ('contact', models.CharField(default=b'', max_length=20)),
                ('postcode', models.CharField(default=b'', max_length=6)),
            ],
            options={
                'db_table': 'Users',
            },
        ),
    ]
