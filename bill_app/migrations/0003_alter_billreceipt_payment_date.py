# Generated by Django 4.2.6 on 2023-10-17 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill_app', '0002_billreceipt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billreceipt',
            name='payment_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
