from django import template
from ..models import Bill_dataset
from ..models import Bill,Bill_details,billing_period
from registered.models import lease
import datetime


register = template.Library()
@register.inclusion_tag("admin/lease_bills/bill_dataset/sublist.html")
def all_leases(count=2):
    data =lease.objects.all()
    return {'data':data}

@register.inclusion_tag('admin/lease_bills/bill_dataset/searchedterms.html')
def searched_terms(query):
    return {
        'query': query
    }


@register.simple_tag
def total_bill(bill_id):
    total = 0
    for item in Bill_details.objects.all().filter(bill_id_id = bill_id):
        total+=((100+item.penalty)*item.fixed_rate*item.official_area/100)
    return format(total, ".2f")


@register.simple_tag
def theperiod(period_id):
    period = ''
    for item in billing_period.objects.all().filter(id = period_id):
        period = item.period
    return period

@register.filter
def cperiod_greater(period_id):
    period = ''
    for item in billing_period.objects.all().filter(id = period_id):
        period = item.period    
    return datetime.date.today().year > period
    