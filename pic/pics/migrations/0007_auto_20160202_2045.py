# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-02 20:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pics', '0006_auto_20160201_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='picturerate',
            name='picture',
            field=models.ManyToManyField(to='pics.Picture'),
        ),
        migrations.AlterUniqueTogether(
            name='picturerate',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='picturerate',
            name='picture',
        ),
    ]
