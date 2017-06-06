# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_auto_20170531_1917'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vpic', models.CharField(max_length=50)),
                ('vtitle', models.CharField(max_length=20)),
                ('vprice', models.DecimalField(max_digits=5, decimal_places=2)),
                ('vunit', models.CharField(default=b'500g', max_length=20)),
                ('vclick', models.IntegerField(default=1)),
                ('vtype', models.IntegerField(default=1)),
                ('vindex', models.IntegerField(default=1)),
                ('vusers', models.ForeignKey(to='Users.Users')),
            ],
            options={
                'db_table': 'VisitInfo',
            },
        ),
    ]
