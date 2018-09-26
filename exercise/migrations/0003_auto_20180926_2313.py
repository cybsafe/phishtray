# Generated by Django 2.0.5 on 2018-09-26 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0002_auto_20180920_1148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='email_reveal_times',
        ),
        migrations.AddField(
            model_name='exerciseemail',
            name='reveal_time',
            field=models.PositiveIntegerField(blank=True, help_text='Time in seconds.', null=True),
        ),
    ]
