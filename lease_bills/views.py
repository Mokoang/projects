from django.shortcuts import render
from registered.models import lease
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def post_data (request):
    # request should be ajax and method should be POST.
  
  return render('change_form.html')

