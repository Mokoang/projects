# Generated by Django 4.1.3 on 2023-01-26 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lease_bills', '0002_alter_bill_billing_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='bill_description',
            field=models.CharField(default='Ground Rent Bill For Jan 2023', max_length=255),
            preserve_default=False,
        ),
    ]