# Generated by Django 3.2.11 on 2023-08-05 15:27

from django.db import migrations

NAMES = {
    "external": {
        "old": "External",
        "new": "External Study (Choose this if you are posting a study link rather using an experiment builder)",
    },
    "efp": {
        "old": "Ember Frame Player (default)",
        "new": "Lookit/Ember Frame Player (Default experiment builder)",
    },
}


def study_type_names(apps, from_key, to_key):
    study_type = apps.get_model("studies", "StudyType")

    # EFP name field
    efp = study_type.objects.get(name=NAMES["efp"][from_key])
    efp.name = NAMES["efp"][to_key]
    efp.save()

    # External name field
    external = study_type.objects.get(name=NAMES["external"][from_key])
    external.name = NAMES["external"][to_key]
    external.save()


def update_study_type_names(apps, schema_editor):
    """Update the display names for study types."""
    study_type_names(apps, "old", "new")


def revert_study_type_names(apps, schema_editor):
    """Update the display names for study types."""
    study_type_names(apps, "new", "old")


class Migration(migrations.Migration):
    dependencies = [
        ("studies", "0092_allow_null_video_pipe_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="studytype",
            name="configuration",
        ),
        migrations.RunPython(
            update_study_type_names, reverse_code=revert_study_type_names
        ),
    ]
