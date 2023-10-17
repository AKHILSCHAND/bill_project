from decimal import Decimal
from django.db import models

# Create your models here.


class Bill(models.Model):
    party_id = models.IntegerField()
    bill_number = models.IntegerField(unique=True)
    bill_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bill_file = models.FileField(upload_to='bills/')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def autosave_paymntamt(self, *args, **kwargs):
        if self.bill_amount is not None and self.paid_amount is not None:
            self.payment_amount = Decimal(self.bill_amount) - Decimal(self.paid_amount)
        super(Bill, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.party_id)
    

class Payment(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    payment_date = models.DateField()
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    PAYMENT_MODE_CHOICES = (
        ('Cash', 'Cash'),
        ('Credit', 'Credit'),
        ('Online', 'Online'),
    )
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODE_CHOICES)
    payment_remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return  str(self.bill.id)



