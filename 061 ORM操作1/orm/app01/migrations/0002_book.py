# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-06-24 08:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
