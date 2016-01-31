# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-31 15:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to=settings.AUTH_USER_MODEL),
        ),
    ]
