from django.contrib import admin
from .models import lease, surrendered_lease,adjusted_area,alter_LandUse,Landuse_Type,lease_details
from lease_bills.models import Bill_dataset
from django_select2 import forms as s2forms
from django.db.models import Q
from django.contrib.auth.models import User, Group
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget, DateWidget
from import_export import resources, fields
from import_export.fields import Field
import datetime
from django.db.models import Q
from django.db import connection
from reference_tables.models import billing_period
from reference_tables.models import reference_table
import re
from datetime import  date
from django.utils.html import format_html
from django.urls import reverse
from django.urls import include, path
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.admin.templatetags import admin_modify
from .forms import leaseForm, surrendered_leaseForm,alter_landuseForm,Landuse_choicesForm,adjusted_areasForm,lease_detailsForm
from .resources import LeaseAdminResource,slAdminResource,adjustareaAdminResource,alterlanduseAdminResource
from django.http import HttpResponseRedirect
from django.shortcuts import redirect


submit_row = admin_modify.submit_row
def submit_row_custom(context):
    ctx = submit_row(context)
    ctx['show_save_and_add_another'] = False
    ctx['show_save_and_continue'] = False
    return ctx
admin_modify.submit_row = submit_row_custom


#@admin.register(lease)        
class leaseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
  
  def get_queryset(self, request):
    queryset = super().get_queryset(request).select_related('landuse_type')
    return queryset

  form             =leaseForm
  fields           =  ['lease_number', 'landuse_type',('area','area_units'),'zone_number','registration_date','lastpayment_date','lease_holder','phone_number','address','district']
  readonly_fields  = ['area_units',]       
  list_display     = ('lease_number','registration_date','lastpayment_period','Area','zone_number','lease_holder','landuse_type','controls')
  list_filter      = ('landuse_type','tag')
  resource_class   = LeaseAdminResource
  exclude = ('lease_status',)
  search_fields = ['registration_date','lastpayment_date','lastpayment_period','lease_number','landuse_type__landuse', 'zone_number','area','lease_history','lease_holder','address','district']
  list_per_page = 50
  list_display_links = None
  

  class Meta:
    model = lease

  def controls(self, obj):
    edit_url = reverse('admin:registered_lease_change', args=[obj.id])
    details_url = reverse('lease_information', kwargs={'lease_id': obj.id})  # Corrected line
    edit_button    = format_html('<a class="button" href="{}" title="Edit">✏️</a>', edit_url)
    details_button = format_html('<a class="button" href="{}" title="Details">📖</a>', details_url)
    return format_html('{} | {}', details_button, edit_button)

  #units
  def Area(self,obj):
    final_units = f'{obj.area} {obj.area_units}'
    if(obj.area_units=='sq_m'):
      final_units =f'{obj.area} m\N{SUPERSCRIPT TWO}'
    return final_units
    
  class Media:
    js = ('//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js', # jquery
            'registered/js/admin.js',   # app static folder
    )
  

  def Action(self,obj):
    view_name = "admin:{}_{}_hello".format(obj._meta.app_label, obj._meta.model_name)
    link      = reverse(view_name, args=[obj.pk])
    html      = '<input type="button" onclick="location.href=\'{}\'" value="Delete" />'.format(link)
    return format_html(html)  



  def has_delete_permission(self, request, obj=None):
    return False
    

  # def has_add_permission(self, request, obj=billing_period.objects.all()):
  #   has_permission  = True
  #   for data in billing_period.objects.all().filter(period=date.today().year).order_by('-id')[:1]:
  #     if data.period_state=='I': #verified
  #       has_permission = False
  #   return has_permission
  

  def has_import_permission(self, request, obj=None):
    has_permission  = True
    for data in billing_period.objects.all().filter(period=date.today().year).order_by('-id')[:1]:
      if data.period_state=='I': #verified
        has_permission = False
    return has_permission

  def has_export_permission(self, request, obj=None):
    has_permission  = True
    for data in billing_period.objects.filter(period=date.today().year).order_by('-id')[:1]:
      if data.period_state=='I': #verified
        has_permission = False
    return has_permission


  def get_actions(self, request):
    actions = super(leaseAdmin, self).get_actions(request)
    for data in billing_period.objects.all().filter(period=date.today().year).order_by('-id')[:1]:
      if data.bill_data_set==True or data.period_state==True:
        del actions['send_for_billing']
    return actions

  #units
  def Current_area(self,obj):
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

  def response_add(self, request, obj):
    if "_continue" in request.POST:
      return super().response_change(request, obj)
    else:
      lease_id = obj.id
      return redirect(reverse('lease_detailz', kwargs={'lease_id': lease_id}))  

  def response_change(self, request, obj):
    if "_continue" in request.POST:
      return super().response_change(request, obj)
    else:
      lease_id = obj.id
      return redirect(reverse('lease_detailz', kwargs={'lease_id': lease_id})) 

admin.site.register(lease,leaseAdmin)  
  
##########=============surrendered_lease Model=============#########
@admin.register(surrendered_lease)   
class surrenderedleaseAdmin(ImportExportModelAdmin,admin.ModelAdmin):
  form=surrendered_leaseForm
  
  actions = None
  extra = 5
  list_display = ('Lease', 'surrender_date','comments')
  
  class meta:
    model = surrendered_lease
   
  resource_class = slAdminResource   

  def Lease(self,obj):
    return obj.lease_number

  def has_change_permission(self, request, obj=None):
    return False

  def has_delete_permission(self, request, obj=None):
    return False

  search_fields = ('lease_number__lease_number', 'surrender_date')
  list_per_page = 10

  class Media:
    js = ('//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js', # jquery
              'registered/js/surrender_lease.js',   # app static folder
          )

# @admin.register(lease_details)   
# class leasedetailsAdmin(admin.ModelAdmin):
  # form         = lease_detailsForm
  # list_display = ('Lease','period','zone_number','Area','landuse_type','fixed_rate','penalty')
  # fields       = ['lease_number','period', 'landuse_type',('area','area_units'),'zone_number','fixed_rate','penalty']
  # ordering     = ['lease_number']
  
  # class meta:
    # model = lease_details
    # readonly_fields = ['area_units',]  

  # def Lease(self,obj):
    # return obj.lease_number

  # units
  # def Area(self,obj):
    # final_units = f'{obj.area} {obj.area_units}'
    # if(obj.area_units=='sq_m'):
      # final_units =f'{obj.area} m\N{SUPERSCRIPT TWO}'
    # return final_units

  # def has_delete_permission(self, request, obj=None):
    # return False

  # def has_edit_permission(self, request, obj=None):
    # return False

  # def has_add_permission(self, request, obj=None):
    # return False


  # def get_readonly_fields(self, request, obj=None):
      # if obj:  # If the object exists, make the lease number field read-only
          # return ['lease_number']  # Replace 'lease_number' with the name of your lease number field
      # return []

  # def get_queryset(self, request):
    # qs = super().get_queryset(request)

    # Joining the lease model with lease_details using ForeignKey
    # qs = qs.filter(lease_number__lease_status='A')

    # return qs
  
  # search_fields = ('lease_number__lease_number',)
  # list_per_page = 10 

  # class Media:
    # js = ('//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js', # jquery
              # 'registered/js/lease_details.js',   # app static folder
          # )


   
@admin.register(adjusted_area)        
class adjustedreasAdmin(ImportExportModelAdmin, admin.ModelAdmin):
  form=adjusted_areasForm
  list_display = ('lease_number','Description','Area', 'record_date')
  exclude = ('description',)
  search_fields = ('lease_number__lease_number', 'proposed_area','area_units','comments','record_date')
  resource_class = adjustareaAdminResource
  def Description(self,obj):
    return obj.description
  
  class Media:
    js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js', # jquery
            'registered/js/modifyarea.js',   # app static folder
        )



  def Area(self,obj):
    final_units = f'{obj.proposed_area} {obj.area_units}'
    if(obj.area_units=='sq_m'):
      final_units =f'{obj.proposed_area} m\N{SUPERSCRIPT TWO}'
    return final_units

  def has_change_permission(self, request, obj=None):
    return False

  def has_delete_permission(self, request, obj=None):
    return False


# ----------------------------------------------------------------------------------
  def has_add_permission(self, request, obj=billing_period.objects.all()):
    has_permission  = True
    return has_permission


  def has_import_permission(self, request, obj=None):
    has_permission  = True
    return has_permission

def hello():
  return 'hello world'

@admin.register(alter_LandUse)        
class alterLandUseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
  form         = alter_landuseForm
  list_display = ('lease_number', 'Description','proposed_land_use','record_date')
  exclude = ('description',)
  search_fields = ('lease_number__lease_number','proposed_land_use__landuse','comments','record_date',)
  resource_class = alterlanduseAdminResource
  
  def Description(self,obj):
    return obj.description

  def has_change_permission(self, request, obj=None):
    return False

  def has_delete_permission(self, request, obj=None):
    return False  

  class Media:
    js = ('//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js', # jquery
          'registered/js/changelanduse.js',   # app static folder
        )

# ----------------------------------------------------------------------------------
  def has_add_permission(self, request, obj=billing_period.objects.all()):
    has_permission  = True
    return has_permission


  def has_import_permission(self, request, obj=None):
    has_permission  = True
    return has_permission


admin.site.unregister(Group)

