# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-06-24 10:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0016_auto_20190624_1010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='pub',
        ),
    ]
