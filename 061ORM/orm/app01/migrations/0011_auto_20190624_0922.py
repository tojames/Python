# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-06-24 09:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0010_auto_20190624_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(db_column='username', help_text='xxx', max_length=32),
        ),
    ]