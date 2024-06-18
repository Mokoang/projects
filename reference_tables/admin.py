from django.contrib import admin
from .models import reference_table,Landuse_Type,billing_period
from django.contrib import admin
from search_placeholder import ModelAdmin
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
from reference_tables.models import Landuse_Type
from .forms import referencetableForm,Landuse_choicesForm,bpForm
from .resources import rtAdminResource
from IPython.display import display, Math
from django.contrib.admin.options import ModelAdmin, csrf_protect_m
from registered.admin import leaseAdmin
from admin_extra_buttons.api import ExtraButtonsMixin, button, confirm_action, link, view
from admin_extra_buttons.utils import HttpResponseRedirectToReferrer
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
def get_super(x):
  normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
  super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
  res = x.maketrans(''.join(normal), ''.join(super_s))
  return x.translate(res)
# Register your models here.
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

@admin.register(Landuse_Type)        
class LandusechoicesAdmin(admin.ModelAdmin):
  form         = Landuse_choicesForm
  list_display = ['landuse','landuse_code']    
  ordering = ['landuse']
  
  def has_change_permission(self, request, obj=None):
    return False

  def has_delete_permission(self, request, obj=None):
    return False

  class Media:
    js = ('//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js', # jquery
          'registered/js/landusetype.js',   # app static folder
    )

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
