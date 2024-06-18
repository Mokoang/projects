"""Billing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from . import views
from django.views.decorators.csrf import csrf_protect
from .models import Bill_dataset
#import reporting

#reporting.autodiscover() 
app_name = 'lease_bills'

urlpatterns = [
  # Your other URL patterns here
  path('bill/<int:pk>/save-custom-data/', views.save_custom_data, name='save_custom_data'),
  #path('lease_bills/bill/select_leases/', views.select_leases, name='select_leases'),
]