from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('unpaid_bills', views.unpaid_bills, name='unpaid_bills'),
    path('payment_details', views.payment_details, name='payment_details'),
]
