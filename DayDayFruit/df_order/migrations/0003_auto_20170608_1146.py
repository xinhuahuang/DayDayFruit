# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_order', '0002_orderinfo_opaytype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderinfo',
            old_name='otaotal',
            new_name='ototal',
        ),
    ]
