# Generated by Django 2.2.6 on 2019-11-15 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('participant', '0003_auto_20190920_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercise.Exercise'),
        ),
    ]
