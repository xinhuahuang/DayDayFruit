# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_order', '0003_auto_20170608_1146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdetailinfo',
            name='unit',
        ),
        migrations.AddField(
            model_name='orderdetailinfo',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
