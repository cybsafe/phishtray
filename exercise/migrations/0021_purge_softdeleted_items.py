from django.db import migrations
from exercise.models import (
    Exercise,
    ExerciseTask,
    ExerciseFile,
    ExerciseEmailReply,
    ExerciseEmail,
    ExerciseWebPage,
    DemographicsInfo
)


def purge_soft_deleted_items(_app, _schema_editor):
    models = (
        Exercise,
        ExerciseTask,
        ExerciseFile,
        ExerciseEmailReply,
        ExerciseEmail,
        ExerciseWebPage,
        DemographicsInfo
    )

    print("\n----")
    for model in models:
        print(f"Purging {model.all_objects.exclude(deleted_at=None).count()} soft deleted {model.__name__} records.")
        model.all_objects.exclude(deleted_at=None).hard_delete()


class Migration(migrations.Migration):

    dependencies = [
        ('participant', '0004_auto_20191115_1121'),
        ('exercise', '0020_auto_20191108_1355'),
    ]

    operations = [
        migrations.RunPython(purge_soft_deleted_items)
    ]
