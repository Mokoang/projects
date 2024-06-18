from django import template
from ..models import lease,Landuse_Type
from reference_tables.models import reference_table          
from django.db.models import Count
from django.db.models.functions import ExtractYear

register = template.Library()

@register.simple_tag
def total_leases():
    return lease.objects.count()

@register.simple_tag
def surrendered_leases():
    return lease.objects.filter(lease_status = 'I').count()

@register.simple_tag
def total_landuse():
    return Landuse_Type.objects.count()

@register.simple_tag
def active_leases():
    return lease.objects.filter(lease_status = 'A').count()


@register.simple_tag
def graph_labels():
    lease_years = lease.objects \
        .annotate(year=ExtractYear('registration_date')) \
        .values('year') \
        .distinct() \
        .order_by('-year')[:5]

    labels = [lease['year'] for lease in lease_years]

    return labels

@register.simple_tag
def graph_data():
    lease_years = lease.objects \
        .annotate(year=ExtractYear('registration_date')) \
        .values('year') \
        .annotate(count=Count('id')) \
        .order_by('-year')[:5]

    labels = [lease['year'] for lease in lease_years]
    data = [lease['count'] for lease in lease_years]

    return data



@register.simple_tag
def get_landuses():
    thedata = {}
    for data in Landuse_Type.objects.all():
        thedata[data.id] = data.landuse

    return thedata    

@register.simple_tag
def get_fixedrates(landusetype,zonenumber,period):
    fixedrate = 0
    for data in reference_table.objects.filter(Landuse_Type=landusetype).filter(zone_number=zonenumber):
        if data.period == period:
            fixedrate = data.fixed_rate
    return fixedrate     

