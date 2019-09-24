# Generated by Django 2.2.5 on 2019-09-24 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0004_auto_20181017_1035'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='demographicsinfo',
            options={'verbose_name_plural': 'Demographic Info'},
        ),
        migrations.AlterModelOptions(
            name='exerciseemailproperties',
            options={'verbose_name_plural': 'Exercise email properties'},
        ),
        migrations.AlterModelOptions(
            name='exercisewebpages',
            options={'verbose_name_plural': 'Exercise web pages'},
        ),
        migrations.AddField(
            model_name='exerciseemail',
            name='phishing_explained',
            field=models.TextField(blank=True, null=True),
        ),
    ]
