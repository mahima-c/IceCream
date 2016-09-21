# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-21 17:26
from __future__ import unicode_literals

import Core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0030_auto_20160902_0140'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='fee_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='registration',
            name='student_number',
            field=models.CharField(max_length=8, validators=[Core.models.student_number_validator]),
        ),
    ]
