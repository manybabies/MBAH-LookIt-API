# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-25 15:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("accounts", "0027_auto_20170824_1800")]

    operations = [
        migrations.AlterField(
            model_name="demographicdata",
            name="number_of_books",
            field=models.IntegerField(blank=True, default=None, null=True),
        )
    ]
