# Generated by Django 4.1.6 on 2023-03-31 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lease_bills', '0004_remove_billdata_landuse_billdataset_id_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bill',
            unique_together={('lease_number', 'window_period')},
        ),
    ]
