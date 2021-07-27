# Generated by Django 2.2.11 on 2021-07-27 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("exercise", "0024_auto_20191208_2326"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exerciseemail",
            name="belongs_to",
            field=models.ForeignKey(
                blank=True,
                help_text="Emails need to belong to another email or themselves to count as threads.<br>Please note, emails that are not part of a thread will not be shown during the exercise.",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="exercise.ExerciseEmail",
            ),
        ),
    ]
