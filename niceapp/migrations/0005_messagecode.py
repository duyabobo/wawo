# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-31 01:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('niceapp', '0004_userrelation'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageCode',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='niceapp.BaseModel')),
                ('usage', models.IntegerField(default=0, verbose_name='\u7528\u9014\uff1a0\u767b\u9646\uff0c1\u63a8\u8350\u901a\u77e5\uff0c2...')),
                ('mobile', models.IntegerField(default=0, verbose_name='\u624b\u673a\u53f7')),
                ('code', models.IntegerField(default=0, verbose_name='\u56db\u4f4d\u77ed\u4fe1\u7801')),
            ],
            bases=('niceapp.basemodel',),
        ),
    ]
