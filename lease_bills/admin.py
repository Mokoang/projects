from django.contrib import admin
from search_placeholder import ModelAdmin
from .models import reference_table, Bill,Bill_details,Bill_finale
from django import forms
from django_select2 import forms as s2forms
from django.db.models import Q
from django.contrib.auth.models import User, Group
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget, DateWidget
from import_export import resources, fields
from import_export.fields import Field
from django.contrib.auth.mixins import PermissionRequiredMixin
import datetime
import re
from django.db import connection
from datetime import  date
from django.utils.html import format_html
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.urls import include, path
from registered.models import lease,Landuse_Type,alter_LandUse


# lease Form
class referencetableForm(forms.ModelForm ):
    
    class Meta:
        model = reference_table
        fields = ['landuse_type','zone_number','period','fixed_rate','penalty']

class BillFinaleForm(forms.ModelForm ):
    description =forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = Bill_finale
        fields = ['closing_date','description']


class invoiceForm(forms.ModelForm):

  class Meta:
    model   = Bill
    fields = ['billing_date','bill_description','lease_number','balance']
    exclude = ['lease_number','balance']


#This class is used to define the import / export functions
class rtAdminResource(resources.ModelResource):
  landuse_type        = Field(column_name='Lease number',attribute='landuse_type', widget=ForeignKeyWidget(Landuse_Type, field='landuse')) 
  zone_number         = Field(attribute='zone_number', column_name = 'Zone Number')
  fixed_rate          = Field(attribute='fixed_rate', column_name = 'Fixed Rate')
  penalty             = Field(attribute='penalty', column_name = 'Penalty (%)')

  class Meta:  
    model            = reference_table
    fields           = ('landuse_type','zone_number','fixed_rate','penalty','period')
    export_order     = ('landuse_type','zone_number','fixed_rate','penalty','period')
    exclude          = ('id',)
    import_id_fields = ('landuse_type','zone_number','period')
    skip_unchanged   = True
    report_skipped   = True

@admin.register(reference_table)        
class referencetableAdmin(ImportExportModelAdmin, admin.ModelAdmin):
  form               = referencetableForm
  list_display       = ['record_date','landuse_type','zone_number','period','fixed_rate','Penalty']
  ordering           = ["-record_date","-period",]
  resource_class     = rtAdminResource        
  search_fields  = ['record_date','landuse_type__landuse','zone_number','period','fixed_rate','penalty']
  list_per_page  = 10

  class Meta:
    model = reference_table

  def Penalty(self,obj):
    return str(obj.penalty)+" %"  

  def Fixed_rate (self,obj):
    return str(obj.fixed_rate)   

  def Rate_status(self,obj):
    if obj.rate_status=='A':   
        return True
    return False   
  Rate_status.boolean = True   

  def has_change_permission(self, request, obj=None):
    return False

  def has_delete_permission(self, request, obj=None):
    return False

  class Media:
    js = ('//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js', # jquery
            'registered/js/referencetable.js',   # app static folder
        )

class invoiceView(PermissionRequiredMixin, DetailView):
  permission_required = "lease_bills.view_invoice"
  template_name       = "admin/lease_bills/Bill/invoice.html"
  model = Bill

  def get_context_data(self, **kwargs):
    return {
        **super().get_context_data(**kwargs),
        **admin.site.each_context(self.request),
        "opts": self.model._meta,
        "bill_details": Bill_details.objects.all(),
        "thelease":lease.objects.all(),
    }

class detailsView(PermissionRequiredMixin, DetailView):
  permission_required = "lease_bills.view_invoice"
  template_name       = "admin/lease_bills/Bill/details.html"
  model = Bill

  def get_context_data(self, **kwargs):
    return {
        **super().get_context_data(**kwargs),
        **admin.site.each_context(self.request),
        "opts": self.model._meta,
        "thelease": lease.objects.filter(lease_status = 'A'),
        "reference": reference_table.objects.all(),
        "current_year": datetime.date.today().year

    }




@admin.register(Bill)
class invoiceAdmin(admin.ModelAdmin):
  form = invoiceForm
  list_display = ['billing_date','bill_description','invoice_number','lease_number','Balance','Invoice']
  ordering = ['-billing_date']
  
  search_help_text = 'type invoice number'
  search_fields = ['billing_date','bill_description','invoice_number','lease_number__lease_number','Balance']
  list_per_page = 10

  class Meta:
    model = Bill

  class Media:
    js = ('//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js', # jquery
            'registered/js/bill.js',   # app static folder
        )

  """
  def get_queryset(self, request):
    qs = super().get_queryset(request)
    return qs.filter(record_date=datetime.date.today())  
  """
  def get_urls(self):
    return [
      path('<pk>/invoice',  
      self.admin_site.admin_view(invoiceView.as_view()),
      name = f"lease_bills_Bill_invoice",
      ),
      path('<pk>/details',  
      self.admin_site.admin_view(detailsView.as_view()),
      name = f"lease_bills_Bill_details",
      ),
      *super().get_urls(),
    ]
  def Invoice(self,obj: Bill)-> str:
    url  = reverse("admin:lease_bills_Bill_invoice",args=[obj.pk])
    url2 = reverse("admin:lease_bills_Bill_details",args=[obj.pk])
    return format_html(f'<a title="invoice" href="{url}">🧾</a>')  


  def Balance(self,obj):
    return f'M {obj.balance:,.2f}'

  def has_change_permission(self, request, obj=None):
    return False

  def has_delete_permission(self, request, obj=None):
    return False
    

@admin.register(Bill_finale)
class invoiceAdmin(admin.ModelAdmin):
  form = BillFinaleForm
  list_display = ['closing_date','period','description']
  ordering = ['closing_date']
  
  search_fields = ['closing_date','period','description']
  list_per_page = 10

  class Meta:
    model = Bill_finale

  def has_change_permission(self, request, obj=None):
    return False

  def has_delete_permission(self, request, obj=None):
    return False
    

  class Media:
    js = ('//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js', # jquery
            'registered/js/billfinale.js',   # app static folder
        )

