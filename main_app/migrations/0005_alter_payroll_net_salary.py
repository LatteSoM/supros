# Generated by Django 5.0.4 on 2024-11-13 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_document_expiry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payroll',
            name='net_salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]