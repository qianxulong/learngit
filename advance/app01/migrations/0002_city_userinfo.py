# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-07-07 10:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('pwd', models.CharField(default='doushidsb', max_length=32)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('mobile', models.CharField(max_length=11, null=True)),
            ],
        ),
    ]
