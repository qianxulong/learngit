# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-07-08 05:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='city',
            field=models.CharField(max_length=11, null=True),
        ),
    ]
