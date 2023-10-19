from django.contrib import admin
from . models import Bill, Party, Payment
# Register your models here.
admin.site.register(Party)
admin.site.register(Bill)

admin.site.register(Payment)
