# Generated by Django 5.0.4 on 2024-11-22 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_alter_employee_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='last_name',
            field=models.CharField(max_length=255, verbose_name='Фамилия'),
        ),
    ]