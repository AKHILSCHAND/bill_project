# Generated by Django 4.2.6 on 2023-10-17 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill_app', '0008_payment_payment_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
