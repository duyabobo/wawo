# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-31 01:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('niceapp', '0002_auto_20171231_0125'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='city',
            field=models.CharField(default='', max_length=100, verbose_name='\u57ce\u5e02\u540d'),
        ),
    ]