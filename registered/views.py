from django.shortcuts import render
from django.http import HttpResponse
from .models import lease,lease_details
from reference_tables.models import reference_table
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.db import connection
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_protect


def lease_detailz(request,lease_id):
    # Your custom logic here
    lease_data    = lease.objects.get(id=lease_id)
    lease_det     = lease_details.objects.filter(lease_number_id=lease_id).order_by('period')
    fixed_rates   = reference_table.objects.all()

    # Pass the lease object to the template
    context = {
        'lease_data': lease_data,
        'lease_det' : lease_det
    }    
    return render(request, 'custom_page.html',context)

def lease_information(request,lease_id):
    # Your custom logic here
    lease_data    = lease.objects.get(id=lease_id)
    lease_det     = lease_details.objects.filter(lease_number_id=lease_id)
    fixed_rates   = reference_table.objects.all()

    # Pass the lease object to the template
    context = {
        'lease_data': lease_data,
        'lease_det' : lease_det
    }    
    return render(request, 'lease_information.html',context)

@csrf_exempt
def save_data(request, lease_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Check if 'data' is a list
            if not isinstance(data, list):
                raise ValueError("Invalid data format. Expecting a list.")

            with connection.cursor() as cursor:
                for item in data:
                    # Check if all required fields are present in 'item'
                    required_fields = ['zone_number', 'area', 'landuse_type_id', 'fixed_rate', 'penalty', 'id']
                    missing_fields = [field for field in required_fields if field not in item]
                    if missing_fields:
                        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

                    cursor.execute("UPDATE registered_lease_details SET zone_number=%s, area=%s, landuse_type_id=%s, fixed_rate=%s, penalty=%s WHERE id=%s", [item['zone_number'], item['area'], item['landuse_type_id'], item['fixed_rate'], item['penalty'], item['id']])

                try:
                    instance = lease_details.objects.filter(lease_number_id=lease_id).order_by('-id')[0]
                except ObjectDoesNotExist:
                    raise ValueError("No lease details found for the given lease ID.")

                cursor.execute("UPDATE registered_lease SET zone_number=%s, area=%s, landuse_type_id=%s WHERE id=%s", [instance.zone_number, instance.area, instance.landuse_type_id, lease_id])

            # Return a JSON response indicating the success of the operation
            return JsonResponse({'status': 'success'})
        except ValueError as e:
            # Return a JSON response indicating the error
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method. Expecting POST.'})

    
def get_data(request,lease_id):
    # Your logic to retrieve data goes here
    selectedlu    = request.GET.get('selectedlu')
    selectedzone  = request.GET.get('selectedzone')
    period        = request.GET.get('period') 
    data          = {}
    data['found'] = "Not Found"
    for item in reference_table.objects.all().filter(period=period).filter(landuse_type_id=selectedlu).filter(zone_number=selectedzone)[:1]:
        data ['fixed_rate'] = item.fixed_rate
        data['penalty']     = item.penalty        
        data['found']       = "Found"
    return JsonResponse(data)

def index(request):
    # Creating a dictionary with the required attributes
    opts = {
        'app_label': lease,
        'app_config': {
            'verbose_name': 'Your App Verbose Name'  # Replace with your app's verbose name
        }
    }
    context = {
        'opts': opts,
        # Add other context variables here if needed
    }    
    return render(request,"registered/dashboard.html",context)

def leasedetails(request, pk):
    # Retrieve the object to display details
    instance = get_object_or_404(lease, pk=pk)
    
    # Render a template to display the details of the object
    return render(request, 'detail_template.html', {'instance': instance})





# from django.db.models import Sum
# from slick_reporting.views import SlickReportView
# from slick_reporting.fields import SlickReportField
# from .models import lease

# class TotalProductSales(SlickReportView):

    # report_model = lease
    # date_field = 'registration_date'
    # group_by = 'lease_number'
    # columns = ['lease_number',]

    # chart_settings = [{
        # 'type': 'column',
        # 'data_source': ['lease_number'],
        # 'plot_total': False,
        # 'title_source': 'title',

    # }, ]

""" def registration(request):
    return render(request,"registered/registered.html")

def details(request):
    all_leases = lease.objects.all()
    return render(request,"registered/leasedetails.html",{"lease": all_leases})

def dashboard(request):
    return render(request,"registered/dashboard.html")

@csrf_exempt
def savedata(request):
    if request.method=="POST":
        registrationdate = request.POST.get('registrationdate')
        lastpaymentdate  = request.POST.get('lastpaymentdate')
        leasenumber      = request.POST.get('leasenumber')
        zonenumber       = request.POST.get('zonenumber')
        area             = request.POST.get('area')
        areaunit         = request.POST.get('areaunit')
        #validate
        error_message    = None

        #registration date validation...
        if(not registrationdate):
            error_message = "Registration Date cannot be empty!"
                
        if(not lastpaymentdate):
            error_message = "Last Payment Date cannot be empty!"    
    
        #lease number validation
        if(not leasenumber):
            error_message = "Lease Number cannot be empty!"
        elif leasenumber:
            for instance in lease.objects.all():
                if instance.lease_number == leasenumber:
                    error_message= 'Lease Number already exists in the database!'

        #area validation    
        if(not area):
            error_message = "Area cannot be empty!"
        elif area:
            if not area.isdecimal():
                error_message = "Area should be a number"
            elif int(area) <= 0:
                error_message = "Area should be a number greater than zero"     

        if (not error_message):
            leaseform = lease(registration_date = registrationdate,lastpayment_date = lastpaymentdate,lease_number = leasenumber, zone_number = zonenumber,area=area,area_units=areaunit)
 """"""             leaseform.savse()
            return render(request,"registered/registered.html",{"success":"Data Saved Succesfully!"})
        else:
            return render(request,"registered/registered.html",{"error":error_message}) """