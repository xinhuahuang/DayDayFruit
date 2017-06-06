# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_visitinfo'),
        ('df_goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField(default=1)),
                ('is_buy', models.IntegerField(default=0)),
                ('good', models.ForeignKey(to='df_goods.GoodsInfo')),
                ('user', models.ForeignKey(to='Users.Users')),
            ],
        ),
    ]
