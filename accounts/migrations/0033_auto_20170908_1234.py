# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-08 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("accounts", "0032_demographicdata_former_lookit_annual_income")]

    operations = [
        migrations.AlterField(
            model_name="child",
            name="birthday",
            field=models.DateField(blank=True, null=True),
        )
    ]
