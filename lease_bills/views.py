from django.shortcuts import render
from registered.models import lease
from .models import Bill_dataset
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from django.http import JsonResponse

from django.urls import reverse


def my_view(request):
  url = reverse('lease_bills:lease_bills_Bill_save_custom_data')



def save_custom_data(request):
   url = reverse('lease_bills:lease_bills_Bill_save_custom_data')


