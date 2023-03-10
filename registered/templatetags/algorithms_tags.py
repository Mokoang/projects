from django import template
from ..models import lease,Landuse_Type

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
    labels = []
    data   = []
    count  = 0
    for datas in lease.objects.all().order_by('-registration_date'):
   
        if len(labels)<1:
            labels.append(datas.registration_date.year)
            data.append(1)
            count=1
        else:
            if len(labels)<=5:
                if labels[len(labels)-1]==datas.registration_date.year:
                    data[len(data)-1] +=1
                else:
                    if len(labels)<5:
                        labels.append(datas.registration_date.year)
                        data.append(1)
                        count+=1
    return labels  
          
@register.simple_tag
def graph_data():
    labels = []
    data   = []
    count  = 0
    for datas in lease.objects.all().order_by('-registration_date'):
   
        if len(labels)<1:
            labels.append(datas.registration_date.year)
            data.append(1)
            count=1
        else:
            if len(data)<=5:
                if labels[len(labels)-1]==datas.registration_date.year:
                    data[len(data)-1] +=1
                else:
                    if len(data)<5:
                        labels.append(datas.registration_date.year)
                        data.append(1)
                        count+=1
    return data  



