from django.urls import path
from . import views

urlpatterns = [
    path('bill', views.bill, name='bill'),
    path('unpaid_bills', views.unpaid_bills, name='unpaid_bills'),
    path('payment_details', views.payment_details, name='payment_details'),
    path('', views.home, name='home'),
    path('party_billing_aging/<int:party_id>/', views.party_billing_aging, name='party_billing_aging'),
]
