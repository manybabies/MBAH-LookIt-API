# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-12-20 18:03
from __future__ import unicode_literals
import uuid

from django.db import migrations, models


def gen_salt(apps, schema_editor):
    MyModel = apps.get_model("studies", "Study")

    field = None
    try:
        field = MyModel._meta.get_field("salt")
    except:
        pass

    if field:  # Condition on field existing because otherwise Django checks this query
        # will work before the migration is run and gets worried
        for row in MyModel.objects.all():
            row.salt = uuid.uuid4()
            row.save()


class Migration(migrations.Migration):

    dependencies = [("studies", "0055_study_salt")]

    operations = [
        migrations.RunPython(gen_salt, reverse_code=migrations.RunPython.noop)
    ]
