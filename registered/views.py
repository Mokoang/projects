from django.shortcuts import render
from django.http import HttpResponse
from registered.models import lease
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

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