# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-01 19:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pics', '0005_auto_20160201_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picturerate',
            name='picture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pics.Picture'),
        ),
    ]