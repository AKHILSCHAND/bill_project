# Generated by Django 4.2.6 on 2023-10-17 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill_app', '0003_alter_billreceipt_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='party_id',
            field=models.IntegerField(),
        ),
    ]
