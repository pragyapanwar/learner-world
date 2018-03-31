# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-02-28 03:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('register', '0004_auto_20180228_0835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='catid',
        ),
        migrations.AddField(
            model_name='resource',
            name='catid',
            field=models.ManyToManyField(to='register.subcategory'),
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='subid',
        ),
        migrations.AddField(
            model_name='subcategory',
            name='subid',
            field=models.ManyToManyField(to='register.subject'),
        ),
        migrations.RemoveField(
            model_name='subject',
            name='userid',
        ),
        migrations.AddField(
            model_name='subject',
            name='userid',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
