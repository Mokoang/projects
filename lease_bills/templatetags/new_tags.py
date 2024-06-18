from django import template
from ..models import Bill,Bill_details,Bill_payment
from reference_tables.models import billing_period
from registered.models import lease
import datetime
from django.db import connection
from datetime import  date

register = template.Library()
@register.inclusion_tag("admin/lease_bills/bill/sublist.html")
def all_leases(count=2):
    data =lease.objects.filter(send_for_bill=False)

    return {'data':data}

@register.inclusion_tag('admin/lease_bills/bill_dataset/searchedterms.html')
def searched_terms(query):
    return {
        'query': query
    }


@register.simple_tag
def sub_total(bill_id):
    total = 0
    for item in Bill_details.objects.filter(bill_id_id = bill_id).filter(status ='A'):
        if item.period < datetime.date.today().year:
            total+=((100+item.penalty)*item.fixed_rate*item.official_area/100)
        else:
            total+=(item.fixed_rate*item.official_area)

    return format(total, ".2f")


@register.simple_tag
def total_bill(bill_id,lease_number):
    total = 0
    for item in Bill_details.objects.filter(bill_id_id = bill_id).filter(status ='A'):
        if item.period < datetime.date.today().year:
            total +=((cal_penalty(lease_number,item.period))+(item.fixed_rate*item.official_area))
        else:
            total+=(item.fixed_rate*item.official_area)

    totalpaid = get_totalpaid(Bill.objects.get(id=bill_id).lease_number)        
    return format(total-totalpaid, ".2f")


@register.simple_tag
def theperiod(period_id):
    period = ''
    for item in billing_period.objects.all().filter(id = period_id):
        period = item.period
    return period


@register.filter
def cperiod_greater(period):
    return datetime.date.today().year > period

@register.simple_tag
def pperiod_limit(period,lease_number):
    found  = False
    for data in Bill_payment.objects.filter(lease_number = lease.objects.get(lease_number=lease_number).id):
        if data.payment_date.year == period:
            found = True
    return found

@register.simple_tag
def save_top(here):
    a='hete'
    if str(here) == '5':
        for bata in lease.objects.all():
            a = bata.lease_number  
    return lease.objects.filter(id=19).update(lastpayment_period=2019)  

@register.simple_tag
def get_regdate(lease_number):
    for data in lease.objects.filter(lease_number = lease_number):
        regdate = data.registration_date

    return regdate   

@register.simple_tag
def get_lpperiod(lease_number):
    for data in lease.objects.filter(lease_number = lease_number):
        lpp = data.lastpayment_period

    return lpp   

@register.simple_tag
def get_perpaid(lease_number,period):
    total = 0
    for data in Bill_payment.objects.filter(lease_number = lease.objects.get(lease_number=lease_number).id).filter(payment_period=period):
        total +=data.amount_paid
    if total==0:
        return '0.00'    
    return  round(total, 2)

# @register.filter
# def payment_made_in_period(lease_number,period):
#     total = 0
#     total_groundrent = 0
#     total_paid       = 0

#     for data in Bill_payment.objects.filter(lease_number = lease.objects.get(lease_number=lease_number).id).filter(payment_period__lte=period):
#         total +=data.amount_paid

#     for thedata in Bill_details.objects.filter(lease_number=lease.objects.get(lease_number=lease_number).id).filter(period__lte=period):
#         total_groundrent += ((thedata.official_area*thedata.fixed_rate)-total)
#         current_gr        = thedata.official_area*thedata.fixed_rate

@register.filter
def cal_penalty(lease_number,period):

    total_paid      = 0
    total_gr        = 0
    total_pen       = 0
    current_payment = 0
    current_gr      = 0
    curr_pen        = 0
    

    for data in Bill_payment.objects.filter(lease_number = lease.objects.get(lease_number=lease_number).id).filter(payment_period__lte=period):
        total_paid +=data.amount_paid
        if data.payment_period == period:
            current_payment +=data.amount_paid

    for thedata in Bill_details.objects.filter(bill_id=Bill.objects.get(lease_number=lease_number).id).filter(period__lte=period):
        total_gr        += (thedata.official_area*thedata.fixed_rate)
        
        if thedata.period == period:
            current_gr  = thedata.official_area*thedata.fixed_rate
        if total_paid == 0:
            total_pen +=  thedata.official_area*thedata.fixed_rate*thedata.penalty/100
            curr_pen   = thedata.official_area*thedata.fixed_rate*thedata.penalty/100
        else:
            total_grpen = total_gr+total_pen-current_gr
            totalbal    = total_paid - total_grpen

            if totalbal>0:
                total = totalbal-current_gr
                if total < 0:
                    curr_pen = -1*total*thedata.penalty/100
            else:
                curr_pen = thedata.official_area*thedata.fixed_rate*thedata.penalty/100       
    return  round(curr_pen, 2)                    

@register.filter
def cal_penalty_add_groundrent(lease_number,period):

    total_paid      = 0
    total_gr        = 0
    total_pen       = 0
    current_payment = 0
    current_gr      = 0
    curr_pen        = 0
    

    for data in Bill_payment.objects.filter(lease_number = lease.objects.get(lease_number=lease_number).id).filter(payment_period__lte=period):
        total_paid +=data.amount_paid
        if data.payment_period == period:
            current_payment +=data.amount_paid

    for thedata in Bill_details.objects.filter(bill_id=Bill.objects.get(lease_number=lease_number).id).filter(period__lte=period):
        total_gr        += (thedata.official_area*thedata.fixed_rate)
        
        if thedata.period == period:
            current_gr  = thedata.official_area*thedata.fixed_rate
        if total_paid == 0:
            total_pen +=  thedata.official_area*thedata.fixed_rate*thedata.penalty/100
            curr_pen   = thedata.official_area*thedata.fixed_rate*thedata.penalty/100
        else:
            total_grpen = total_gr+total_pen-current_gr
            totalbal    = total_paid - total_grpen

            if totalbal>0:
                total = totalbal-current_gr
                if total < 0:
                    curr_pen = -1*total*thedata.penalty/100
            else:
                curr_pen = thedata.official_area*thedata.fixed_rate*thedata.penalty/100       
    return  round(curr_pen+current_gr, 2)                    

#     return  (total>0)
@register.simple_tag
def get_baldue(lease_number,period,sub_total):
    total = 0
    for data in Bill_payment.objects.filter(lease_number = lease.objects.get(lease_number=lease_number).id).filter(payment_period=period):
        total +=data.amount_paid
    return sub_total-total


@register.simple_tag
def get_totalpaid(lease_number):
    total = 0
    for data in Bill_payment.objects.filter(lease_number = lease.objects.get(lease_number=lease_number).id):
        total +=data.amount_paid
    return total  


@register.simple_tag
def get_leaseholder(lease_number):
    lease_holder = ""
    for data in lease.objects.filter(lease_number=lease_number):
        lease_holder = data.lease_holder
    return lease_holder 

@register.simple_tag
def get_address(lease_number):
    address = ""
    for data in lease.objects.filter(lease_number=lease_number):
        address = data.address
    return address

@register.simple_tag
def get_district(lease_number):
    district = ""
    for data in lease.objects.filter(lease_number=lease_number):
        district = data.district
    return district

@register.simple_tag
def get_end_of_next_fy():
    return date.today().year+1

@register.simple_tag
def get_bill(bill_id):
    return lease.objects.filter(id=bill_id)


@register.filter
def cal_arreas(lease_number,period):
    period = period-1

    total_paid      = 0
    total_gr        = 0
    total_pen       = 0
    current_payment = 0
    current_gr      = 0
    curr_pen        = 0
    

    for data in Bill_payment.objects.filter(lease_number = lease.objects.get(lease_number=lease_number).id).filter(payment_period__lte=period):
        total_paid +=data.amount_paid
        if data.payment_period == period:
            current_payment +=data.amount_paid

    for thedata in Bill_details.objects.filter(bill_id=Bill.objects.get(lease_number=lease_number).id).filter(period__lte=period):
        total_gr        += (thedata.official_area*thedata.fixed_rate)
        
        if thedata.period == period:
            current_gr  = thedata.official_area*thedata.fixed_rate
        if total_paid == 0:
            total_pen +=  thedata.official_area*thedata.fixed_rate*thedata.penalty/100
            curr_pen   = thedata.official_area*thedata.fixed_rate*thedata.penalty/100
        else:
            total_grpen = total_gr+total_pen-current_gr
            totalbal    = total_paid - total_grpen

            if totalbal>0:
                total = totalbal-current_gr
                if total < 0:
                    curr_pen = -1*total*thedata.penalty/100
            else:
                curr_pen = thedata.official_area*thedata.fixed_rate*thedata.penalty/100       
    return  round(curr_pen, 2)                    



@register.filter
def get_per_total(lease_number,period):



    total_paid      = 0
    total_gr        = 0
    total_pen       = 0
    current_payment = 0
    current_gr      = 0
    curr_pen        = 0
    for thedata in Bill_details.objects.filter(bill_id=Bill.objects.get(lease_number=lease_number).id).filter(period__lte=period):
    
        if thedata.period == period:
            current_gr  = thedata.official_area*thedata.fixed_rate
        
    period = period-1
    for data in Bill_payment.objects.filter(lease_number = lease.objects.get(lease_number=lease_number).id).filter(payment_period__lte=period):
        total_paid +=data.amount_paid
        if data.payment_period == period:
            current_payment +=data.amount_paid

    for thedata in Bill_details.objects.filter(bill_id=Bill.objects.get(lease_number=lease_number).id).filter(period__lte=period):
        total_gr        += (thedata.official_area*thedata.fixed_rate)
        
        if total_paid == 0:
            total_pen +=  thedata.official_area*thedata.fixed_rate*thedata.penalty/100
            curr_pen   = thedata.official_area*thedata.fixed_rate*thedata.penalty/100
        else:
            total_grpen = total_gr+total_pen-current_gr
            totalbal    = total_paid - total_grpen

            if totalbal>0:
                total = totalbal-current_gr
                if total < 0:
                    curr_pen = -1*total*thedata.penalty/100
            else:
                curr_pen = thedata.official_area*thedata.fixed_rate*thedata.penalty/100
                       
    return  round(current_gr+curr_pen, 2)                    
