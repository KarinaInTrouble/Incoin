# Generated by Django 4.2.1 on 2023-05-24 04:58

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date',
            field=models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(2023, 5, 24))], verbose_name='Дата выполнения задачи'),
        ),
    ]
