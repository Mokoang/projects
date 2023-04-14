# Generated by Django 4.1.6 on 2023-04-04 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lease_bills', '0006_alter_bill_lease_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='bill_description',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='invoice_number',
        ),
        migrations.RemoveField(
            model_name='bill_details',
            name='invoice_number',
        ),
        migrations.AddField(
            model_name='bill_details',
            name='bill_id',
            field=models.ForeignKey(default=87, on_delete=django.db.models.deletion.CASCADE, to='lease_bills.bill'),
            preserve_default=False,
        ),
    ]
