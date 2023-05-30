# Generated by Django 4.2.1 on 2023-05-24 05:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_task_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата'),
        ),
        migrations.AddField(
            model_name='income',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата'),
        ),
    ]
