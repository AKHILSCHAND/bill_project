import datetime
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Bill, Party, Payment
from django.db.models import F
from datetime import date, timedelta
from django.utils import timezone


# Bills 

def bill(request):
    bills = Bill.objects.all()
    parties = Party.objects.all() 

    if request.method == "POST":
        if "create" in request.POST:
            party_id = request.POST.get("party_id")
            bill_number = request.POST.get("bill_number")
            bill_date = request.POST.get("bill_date")
            bill_amount = request.POST.get("bill_amount")
            paid_amount = request.POST.get("paid_amount")
            bill_file = request.FILES["bill"]

            # Check if a party with the given party_id exists
            party, created = Party.objects.get_or_create(party_id=party_id)

            # Create a new bill
            Bill.objects.create(
                party_id=party,
                bill_number=bill_number,
                bill_date=bill_date,
                bill_amount=bill_amount,
                paid_amount=paid_amount,
                bill_file=bill_file,
            )

            if created:
                messages.success(request, f"Party with Id {party_id} and Bill added successfully.")
            else:
                messages.success(request, "bill added successfully for existing Party.")

        elif "update" in request.POST:
            id = request.POST.get("id")
            party_id = request.POST.get("party_id")
            bill_number = request.POST.get("bill_number")
            bill_date = request.POST.get("bill_date")
            bill_amount = request.POST.get("bill_amount")
            paid_amount = request.POST.get("paid_amount")

            if "bill" in request.FILES:
                bill_file = request.FILES["bill"]
            else:
                existing_bill = Bill.objects.get(id=id)
                bill_file = existing_bill.bill_file

            bill = Bill.objects.get(id=id)
            bill.party_id = party_id
            bill.bill_number = bill_number
            bill.bill_date = bill_date
            bill.bill_amount = bill_amount
            bill.paid_amount = paid_amount
            bill.bill_file = bill_file

            bill.save()
            messages.info(request, "Bill updated successfully")

        elif "delete" in request.POST:
            id = request.POST.get("id")
            Bill.objects.get(id=id).delete()
            messages.success(request, "Bill deleted successfully")         

    
    # Range filter
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    
    if start_date and end_date:
        start_date = timezone.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = timezone.datetime.strptime(end_date, "%Y-%m-%d")
        bills = bills.filter(bill_date__range=[start_date, end_date])
    
    # partyid filter
    party_id = request.GET.get("party_id")
    
    if party_id:
        bills = bills.filter(party_id=party_id)
    
    # Days filter
    due_days = request.GET.get("due_days")
    
    
    if due_days:
        today = date.today()
        due_date = today - timedelta(days=int(due_days))
        bills = bills.filter(bill_date__lte=due_date)
        # print(today)
        # print(due_date_)
    context ={
            "bills": bills,
            "parties": parties,
            }
    
    return render(request, "bill.html", context)

# Unpaid Bills

def unpaid_bills(request):
    bills = Bill.objects.all()
    if request.method == "POST":
        if "paying" in request.POST:
            bill_id = request.POST.get("bill_id")
            print(bill_id)
            payment_amount = request.POST.get("payment_amount")
            payment_mode = request.POST.get("payment_mode")
            payment_remarks = request.POST.get("payment_remarks")

            try:
                bill = Bill.objects.get(id=bill_id)
            except Bill.DoesNotExist:
                messages.error(request, "Bill not found")
                # messages.error(request, f"Bill not found for ID: {bill_id}")
                return redirect('bill')

            try:
                payment_amount = Decimal(payment_amount)
            except ValueError:
                messages.error(request, "Invalid payment amount")
                return redirect('bill')

            new_paid_amount = bill.paid_amount + payment_amount

            payment = Payment(
                bill=bill,
                payment_date=datetime.date.today(),
                payment_amount=payment_amount,
                payment_mode=payment_mode,
                payment_remarks=payment_remarks,
            )
            payment.save()

            bill.paid_amount = new_paid_amount
            bill.save()

            messages.success(request, "Payment recorded successfully")
    # Filter bills where bill_amount - paid_amount > 0
    unpaid_bills = Bill.objects.filter(bill_amount__gt=F('paid_amount'))

    context = {
        'unpaid_bills': unpaid_bills,
        "bills": bills,
    }
    return render(request, 'unpaid_bills.html', context)


def make_payment(request):
    bills = Bill.objects.all()
    if request.method == "POST":
        if "paying" in request.POST:
                bill_id = request.POST.get("bill_id")
                payment_amount = request.POST.get("payment_amount")
                payment_mode = request.POST.get("payment_mode")
                payment_remarks = request.POST.get("payment_remarks")

                try:
                    bill = Bill.objects.get(id=bill_id)
                except Bill.DoesNotExist:
                    messages.error(request, "Bill not found")
                    return redirect('bill')

                try:
                    payment_amount = Decimal(payment_amount)
                except ValueError:
                    messages.error(request, "Invalid payment amount")
                    return redirect('bill')

                new_paid_amount = bill.paid_amount + payment_amount

                payment = Payment(
                    bill=bill,
                    payment_date=datetime.date.today(),
                    payment_amount=payment_amount,
                    payment_mode=payment_mode,
                    payment_remarks=payment_remarks,
                )
                payment.save()

                bill.paid_amount = new_paid_amount
                bill.save()

                messages.success(request, "Payment recorded successfully")

    context = {"bills": bills}
    
    
    return render(request, 'unpaid_bills.html', context)


def payment_details(request):
    payment_details = Payment.objects.all()
    context = {"payment_details": payment_details}
    return render(request, 'payment_details.html', context)


# Home

def home(request):
    parties = Party.objects.all() 

    if request.method == "POST":
        if "create" in request.POST:
            party_id = request.POST.get("party_id")
            party_name = request.POST.get("party_name")
            contact_information = request.POST.get("contact_information")
            address = request.POST.get("address")
            
            party, created = Party.objects.get_or_create(party_id=party_id)
            
            if not created:
                messages.warning(request, f"Warning: Party with the same party ID ({party_id}) already exists.")
            else:
                party.party_name = party_name
                party.contact_information = contact_information
                party.address = address
                party.save()
                messages.success(request, f"{party_name} added successfully.")
            return redirect('home')
    
        if "search" in request.POST:
            party_id = request.POST.get("party_id")  
            try:
                party = Party.objects.get(party_id=party_id)
                
                
                
                bills = Bill.objects.filter(party_id=party)
                # print(bills)

                context = {
                    'party': party,
                    'bills': bills
                }
                
                return render(request, 'home.html', context)
            except Party.DoesNotExist:
                
                messages.warning(request, f"Party with ID ({party_id}) not found. ")


    context = {
        "parties": parties,
    }
    return render(request, 'home.html', context)



# Aging

def party_billing_aging(request):
    party_id = request.GET.get('party_id')

    parties = Party.objects.all()
    aging_data = {}

    if party_id:
        selected_party = Party.objects.get(id=party_id)
        bills = Bill.objects.filter(party_id=party_id)  

        # Calculate aging data 
        total_bills = 0
        less_than_30 = 0
        from_31_to_60 = 0
        from_61_to_90 = 0
        greater_than_90 = 0
        net_amount_due = 0

        today = date.today()
        
        for bill in bills:
            bill_age = (today - bill.bill_date).days
            total_bills += 1
            if bill_age < 30:
                less_than_30 += (bill.bill_amount - bill.paid_amount)
            elif 30 <= bill_age <= 60:
                from_31_to_60 += (bill.bill_amount - bill.paid_amount)
            elif 61 <= bill_age <= 90:
                from_61_to_90 += (bill.bill_amount - bill.paid_amount)
            else:
                greater_than_90 += (bill.bill_amount - bill.paid_amount)
            net_amount_due += (bill.bill_amount - bill.paid_amount)

        aging_data[selected_party.party_name] = {
            'total_bills': total_bills,
            'less_than_30': less_than_30,
            'from_31_to_60': from_31_to_60,
            'from_61_to_90': from_61_to_90,
            'greater_than_90': greater_than_90,
            'net_amount_due': net_amount_due,
        }
    context = {
        # 'party_id': party_id,
        'parties': parties,
        'aging_data': aging_data,
    }

    return render(request, 'party_billing_aging.html', context)