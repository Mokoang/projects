# Generated by Django 4.1.3 on 2023-01-26 10:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lease_bills', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='billing_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]