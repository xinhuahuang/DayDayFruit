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
            name='OrderDetailInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('unit', models.IntegerField()),
                ('goods', models.ForeignKey(to='df_goods.GoodsInfo')),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('oid', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('odate', models.DateTimeField(auto_now_add=True)),
                ('oIsPay', models.BooleanField(default=False)),
                ('otaotal', models.DecimalField(max_digits=6, decimal_places=2)),
                ('oaddress', models.CharField(max_length=150)),
                ('user', models.ForeignKey(to='Users.Users')),
            ],
        ),
        migrations.AddField(
            model_name='orderdetailinfo',
            name='order',
            field=models.ForeignKey(to='df_order.OrderInfo'),
        ),
    ]
