from django import template
from registered.models import lease

register = template.Library()

@register.simple_tag
def regiteredleases():
    registered_lease   ={}
    surrendered_lease  ={}

    for data in lease.objects.all().order_by('registration_date'):
        if data.lease_status=='A' and  data.registration_date.year not in  registered_lease:
            registered_lease[data.registration_date.year] = 1
        elif data.lease_status=='A' and  data.registration_date.year in registered_lease:
            registered_lease[data.registration_date.year]+=1
    return registered_lease 

@register.simple_tag
def unregiteredleases():
    surrendered_lease  ={}

    for data in lease.objects.all().order_by('registration_date'):
        if data.lease_status=='I' and  data.registration_date.year not in surrendered_lease:
            surrendered_lease[data.registration_date.year] = 1
        elif data.lease_status=='I' and  data.registration_date.year in surrendered_lease:
            surrendered_lease[data.registration_date.year]+=1
    return surrendered_lease 


            



