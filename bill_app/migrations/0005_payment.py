# Generated by Django 4.2.6 on 2023-10-17 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bill_app', '0004_alter_bill_party_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField()),
                ('payment_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_mode', models.CharField(choices=[('Cash', 'Cash'), ('Credit', 'Credit'), ('Online', 'Online')], max_length=10)),
                ('payment_remarks', models.TextField(blank=True, null=True)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill_app.bill')),
            ],
        ),
    ]
