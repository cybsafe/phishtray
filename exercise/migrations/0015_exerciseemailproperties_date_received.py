# Generated by Django 2.2.5 on 2019-10-25 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0014_auto_20191024_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='exerciseemailproperties',
            name='date_received',
            field=models.DateTimeField(blank=True, help_text='If date is provided reveal time will be automatically set to 0.', null=True),
        ),
    ]