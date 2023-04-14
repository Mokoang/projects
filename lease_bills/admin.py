from django.contrib import admin
from search_placeholder import ModelAdmin
from .models import reference_table, Bill,Bill_details,billing_period,Bill_dataset,billdata
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
from .forms import referencetableForm,invoiceForm,bpForm
from .resources import rtAdminResource
from IPython.display import display, Math
from django.contrib.admin.options import ModelAdmin, csrf_protect_m
from registered.admin import leaseAdmin
from admin_extra_buttons.api import ExtraButtonsMixin, button, confirm_action, link, view
from admin_extra_buttons.utils import HttpResponseRedirectToReferrer
from django.http import HttpResponse, JsonResponse


@admin.register(reference_table)        
class referencetableAdmin(ImportExportModelAdmin, admin.ModelAdmin):
  
  form               = referencetableForm
  list_display       = ['record_date','landuse_type','zone_number','period','fixed_rate','Penalty']
  ordering           = ["-record_date","-period",]
  resource_class     = rtAdminResource        
  search_fields      = ['record_date','landuse_type__landuse','zone_number','period','fixed_rate','penalty']
  list_per_page      = 10



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
        "billdata":billdata.objects.all(),
        "bill":Bill.objects.all(),
      }

@admin.register(Bill)
class invoiceAdmin(admin.ModelAdmin):
  form = invoiceForm
  list_display = ['lease_number','Bill_reciept',]
  
  search_help_text = 'type invoice number'
  search_fields = ['lease_number__lease_number']
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
    return qs.filter(billing_date=datetime.date.today())  
  """
  def get_urls(self):
    return [
      path('<pk>/lease_number',  
      self.admin_site.admin_view(invoiceView.as_view()),
      name = f"lease_bills_Bill_lease_number",
      ),
      *super().get_urls(),
    ]
  
  def Bill_reciept(self,obj: Bill)-> str:
    url  = reverse("admin:lease_bills_Bill_lease_number",args=[obj.pk])
    return format_html(f'<a title="invoice" href="{url}">🧾</a>')  
  
  def has_change_permission(self, request, obj=None):
    return False

  def has_delete_permission(self, request, obj=None):
    return False
# function to convert to superscript
def get_super(x):
  normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
  super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
  res = x.maketrans(''.join(normal), ''.join(super_s))
  return x.translate(res)


@admin.register(billing_period)        
class lvAdmin( admin.ModelAdmin):

  form = bpForm

  list_display = ['opening_date','closing_date','period','window','state']  
  list_display_links = ()
  #status
  def state(self,obj):
    if obj.period_state=='A':   
      return "Open"
    return "Closed"
  """
  def get_readonly_fields(self, request, obj=None):
    for instance in billing_period.objects.all().order_by("-id")[:1]:
      if instance.period_state == 'A':
          return ['period','period_state']
      else:        
          return ['period_state'] 
  """

  def opening_date(self,obj):
    return obj.billing_period_opening_date

  def closing_date(self,obj):
    return obj.billing_period_closing_date 

  def window(self,obj):
    text = ""
    if str(obj.window_number) ==str(1):
      text = str(obj.window_number)+get_super("st")
    elif str(obj.window_number) ==str(2):
      text = str(obj.window_number)+get_super("nd")
    elif str(obj.window_number) ==str(3):
      text = str(obj.window_number)+get_super("rd") 
    else:
      text = str(obj.window_number)+get_super("th")
    return  text
      
  class  Meta:
    model = billing_period

  def has_delete_permission(self, request, obj=None):
      return False
        
  def has_change_permission(self, request, obj=None):
      return False

  class Media:
    js = ('//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js', # jquery
            'registered/js/billing_period.js',   # app static folder
        )  


@admin.register(Bill_dataset)
class bdAdmin(ExtraButtonsMixin,admin.ModelAdmin):
  """  
  @button(permission='add_bill_dataset',
          change_form=True,
          html_attrs={'style': 'background-color: #0096FF;border-radius: 12px;border: none;color: white;padding: 10px;text-align: center;text-decoration: none;display: inline-block;font-size: 12px;margin: 4px 2px;'})
  def Archives(self, request):
    self.message_user(request, 'Archives called')
    # Optional: returns HttpResponse
    qs = super().get_queryset(request)
    
    return qs.filter(data_state='P')
  """
  change_form_template = 'admin/lease_bills/bill_dataset/change_form.html'
  actions = ['delete_selected']

  list_display = ['registration_date','lastpayment_date','lease_number','landuse_type','zone_number','Area','window_period']

  def window_period(self,obj):
    text = ''
    for data in billing_period.objects.filter(id=obj.period_id):
        text = str(data.window_number)+' - '+str(data.period)
    return text
      
  def has_change_permission(self, request, obj=None):
    return False

  def has_delete_permission(self, request, obj=None):
    return False

  def has_add_permission(self, request, obj=billing_period.objects.all()):
    return False
  # admin.py
  def delete_selected(self, request, queryset):
    queryset.update(data_state='D')
    for instance in Bill_dataset.objects.all().filter(data_state='D'):
      connection.cursor().execute("UPDATE lease_bills_billdata SET billdata = %s WHERE lease_number = %s",[False,instance.lease_number])
      connection.cursor().execute("Delete FROM lease_bills_bill_dataset WHERE lease_number = %s",[instance.lease_number])

  def get_actions(self, request):
    actions = super(bdAdmin, self).get_actions(request)
    for data in billing_period.objects.all().order_by('-id')[:1]:
      if data.period_state=='I':
        del actions['delete_selected']
    return actions
  #units
  def Area(self,obj):
    final_units = f'{obj.area} {obj.area_units}'
    if(obj.area_units=='sq_m'):
      final_units =f'{obj.area} m\N{SUPERSCRIPT TWO}'
    return final_units  

  def get_queryset(self, request):
    qs = super().get_queryset(request)
    return qs.filter(data_state='P')
# myapp/admin.py

from django.contrib import admin
from django.contrib.auth.decorators import login_required

@login_required
def post_data(request):
    # perform some custom action
    # ...
    return render('change_form.html')


   

@admin.register(billdata)        
class billdataAdmin(admin.ModelAdmin):
  actions = ['send_for_billing']
  #readonly_fields = ['area_units',]       
  list_display = ('registration_date','lastpayment_date','lastpayment_period','lease_number','landuse_type', 'zone_number','Area','status')
  #list_filter = ("lease_status", )
  #exclude = ('lease_status',)
  #search_fields = ['registration_date','lastpayment_date','lastpayment_period','lease_number','landuse_type__landuse', 'zone_number','area',]
  list_per_page = 10

  def registration_date(self,obj):
      return list(lease.objects.all())

  #units
  def Area(self,obj):
    final_units = f'{obj.area} {obj.area_units}'
    if(obj.area_units=='sq_m'):
      final_units =f'{obj.area} m\N{SUPERSCRIPT TWO}'
    return final_units


  #status
  def status(self,obj):
    if obj.lease_status=='A':   
        return True
    return False   
  status.boolean = True

  def has_change_permission(self, request, obj=None):
    return False

  def has_delete_permission(self, request, obj=None):
    return False
  
  def has_add_permission(self, request, obj=billing_period.objects.all()):
    return False
  
  def send_for_billing(self, request, queryset):
    verperid = 0

    for thedata in billing_period.objects.all().order_by("-id")[:1]:
      verperid = thedata.id
    for instance in queryset:
      connection.cursor().execute("UPDATE  lease_bills_billdata SET billdata =  %s WHERE lease_number = %s",[True,instance.lease_number])  
      connection.cursor().execute("INSERT INTO testing (name) VALUES (%s)",[instance.lease_number])
      connection.cursor().execute("INSERT INTO lease_bills_Bill_dataset (record_date,lease_number,zone_number,lastpayment_period,registration_date,lastpayment_date,window_period_id,landuse_type_id,area,area_units,data_state) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[date.today(),instance.lease_number,instance.zone_number,instance.lastpayment_period,instance.registration_date,instance.lastpayment_date,verperid,instance.landuse_type_id,instance.area,instance.area_units,'P'])
    #send for billing

  def get_queryset(self, request):
    qs = super().get_queryset(request)
    return qs.filter(billdata=False).filter(lease_status='A')
  def get_actions(self, request):
    actions = super(billdataAdmin, self).get_actions(request)
    present = False
    for data in billing_period.objects.all().order_by('-id')[:1]:
      present = True
      if data.period_state=='I':
        del actions['send_for_billing']
    if not present:
      del actions['send_for_billing']

    return actions