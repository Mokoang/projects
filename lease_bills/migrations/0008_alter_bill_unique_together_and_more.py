# Generated by Django 4.1.6 on 2023-04-05 08:43

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lease_bills', '0007_remove_bill_bill_description_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bill',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='bill_details',
            name='period',
        ),
        migrations.AddField(
            model_name='bill',
            name='bill_description',
            field=models.CharField(default='desc', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bill_details',
            name='bill_description',
            field=models.CharField(default='desc', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bill_details',
            name='window_period',
            field=models.ForeignKey(default=14, limit_choices_to=models.Q(('period_state', 'I')), on_delete=django.db.models.deletion.CASCADE, to='lease_bills.billing_period'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bill',
            name='lease_number',
            field=models.TextField(max_length=50, unique=True, validators=[django.core.validators.MinLengthValidator(7)]),
        ),
        migrations.RemoveField(
            model_name='bill',
            name='balance',
        ),
    ]
