from django.contrib import admin
from .models import lease, surrendered_lease,adjusted_area,alter_LandUse,Landuse_Type
from django import forms
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
from lease_bills.models import reference_table
import re
from datetime import  date
from django.utils.html import format_html
from django.urls import reverse
from django.urls import include, path
from django.contrib.auth.mixins import PermissionRequiredMixin



# lease Form
class leaseForm( forms.ModelForm ):
  lease_number = forms.CharField(widget=forms.TextInput(attrs={'id':'myField'}), required=True)
  #land_use     = forms.ModelChoiceField(queryset=Landuse_Type.objects.all())
  area_units   = forms.CharField(widget=forms.HiddenInput(), label='')

  class Meta:
      model = lease
      fields = ['lease_number', 'landuse_type','zone_number','registration_date','lastpayment_date','lastpayment_period','area','area_units']
      labels ={"area_units":"",}
      field_order = ['lease_number', 'landuse_type','area','area_units','zone_number','registration_date','lastpayment_date','lastpayment_period']

      def __init__(self, *args, **kwargs):
        self.order_fields(self.Meta.fields)

#This class is used to define the import / export functions
class LeaseAdminResource(resources.ModelResource):

  registration_date = Field(attribute='registration_date', column_name = 'Registration date', widget = DateWidget("%d/%m/%Y"))
  lastpayment_date  = Field(attribute='lastpayment_date', column_name = 'Lastpayment date', widget = DateWidget("%d/%m/%Y"))
  lease_number      = Field(attribute='lease_number',column_name = 'Lease number')
  zone_number       = Field(attribute='zone_number',column_name = 'Zone number')
  area              = Field(attribute='area',column_name = 'Area')
  area_units        = Field(attribute='area_units',column_name = 'Area units')
  landuse_type      = Field(attribute='landuse_type',column_name = 'Landuse type')

  class Meta:
    model = lease
    fields = ('lease_number', 'zone_number','area','area_units','landuse_type','registration_date','lastpayment_date')
    export_order =  ('registration_date','lease_number', 'zone_number','area','area_units','landuse_type','lastpayment_date')
    exclude = ('id','lease_status',)
    import_id_fields = ('lease_number',)
    skip_unchanged = True
    report_skipped = True

  # This class defines when top skip the row with the following conditions whne importing
  def skip_row(self, instance, original, row, import_validation_errors=None):
   
    #check that we do not have the same lease number being exported
    skip = False
  
    if original.lease_number:
        skip = True
    #check that our lease number is correctly formated 
    
    if instance.lease_number.rfind('-',5,6)!=5 or instance.lease_number.count('-')!=1:
      skip = True
    #check are
    if not isinstance(float(instance.area),float) or float(instance.area)<=0:
      skip = True 
    

    #chekc the area units...
    
    if instance.area_units!='m\u00b2' or instance.area_units=='':
      skip = True

    
    #check the zone number
    if int(instance.zone_number)<1 or int(instance.zone_number)>6:
      skip = True 
    
    #check the land use
    found = False
    for instance2 in Landuse_Type.objects.all():
      if instance.landuse_type == instance2.landuse:
        found = True

    if not found:
      skip = True

    #check Date.......
  
    if(str(instance.registration_date) != datetime.datetime.strptime(str(instance.registration_date), '%Y-%m-%d').strftime('%Y-%m-%d')) :
      skip = True

    if(str(instance.lastpayment_date )!= datetime.datetime.strptime(str(instance.lastpayment_date), '%Y-%m-%d').strftime('%Y-%m-%d')) :
      skip = False     
    return skip

class surrendered_leaseForm( forms.ModelForm ):
  comments = forms.CharField(widget=forms.Textarea, required=False)
  class Meta:
    model = surrendered_lease
    fields = '__all__'

class slAdminResource(resources.ModelResource):
  surrender_date = Field(attribute='surrender_date', column_name = 'Surrender date', widget = DateWidget("%d/%m/%Y"))
  lease_number   = Field(attribute='lease_number', column_name = 'Lease number')
  comments       = Field(attribute='comments', column_name = 'Comments')
  lease_number   = Field(column_name='Lease number', attribute='lease_number', widget=ForeignKeyWidget(lease, field='lease_number'))
  
  class Meta:  
    model = surrendered_lease
    fields = ('surrender_date','lease_number','comments')
    export_order = ('surrender_date','lease_number' ,'comments')
    exclude = ('id',)
    import_id_fields = ('lease_number',)

  def skip_row(self, instance, original, row, import_validation_errors=None):
    skip   = False
    located  = False

        #check that our lease number is correctly formated
    for theinstance in surrendered_lease.objects.all():
      if theinstance.lease_number == instance.lease_number:
           located = True

    if located:
      skip = True       
    
    if instance.lease_number.lease_number.rfind('-',5,6)!=5 or instance.lease_number.lease_number.count('-')!=1:
      skip = True

    if(str(instance.surrender_date) != datetime.datetime.strptime(str(instance.surrender_date), '%Y-%m-%d').strftime('%Y-%m-%d')) :
      skip = True

     
    return skip



class adjusted_areasForm( forms.ModelForm ):
  comments = forms.CharField(widget=forms.Textarea, required=False)
  class Meta:
      model = adjusted_area
      fields = '__all__'


class alter_landuseForm( forms.ModelForm ):
  comments              = forms.CharField(widget=forms.Textarea, required=False)
  proposed_land_use     = forms.ModelChoiceField(queryset=Landuse_Type.objects.filter(~Q(landuse = alter_LandUse.proposed_land_use)))
  class Meta:
      model = alter_LandUse
      fields = '__all__'        


class Landuse_choicesForm( forms.ModelForm ):
  class Meta:
    model = Landuse_Type
    fields = '__all__'        





@admin.register(lease)        
class leaseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
  form=leaseForm
  fields =   ['lease_number', 'landuse_type',('area','area_units'),'zone_number','registration_date','lastpayment_date','lastpayment_period']
  readonly_fields = ['area_units',]       
  list_display = ('registration_date','lastpayment_date','lastpayment_period','lease_number','landuse_type', 'zone_number','Area','status')
  resource_class = LeaseAdminResource
  exclude = ('lease_status',)
  search_fields = ['registration_date','lastpayment_date','lastpayment_period','lease_number','landuse_type__landuse', 'zone_number','area','status']
  list_per_page = 10
  class Meta:
    model = lease

  def balance(self,obj):
    total_balance  = 0
    with connection.cursor() as cursor:
      #q1 = cursor.execute("SELECT * FROM lease_bills_reference_table WHERE landuse_type_id = %s and zone_number = %s",[obj.landuse_type.id,obj.zone_number])
      totalyears = (date.today().year - obj.lastpayment_date.year)+1
      #current_lease.year
      
      for instance in reference_table.objects.raw("SELECT * FROM lease_bills_reference_table WHERE landuse_type_id = %s and zone_number = %s",[obj.landuse_type.id,obj.zone_number]):
        total_balance =  (instance.fixed_rate*obj.area)*totalyears
        
    return f'M {total_balance:,.2f}'

  class Media:
    js = ('//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js', # jquery
            'registered/js/admin.js',   # app static folder
        )
  

  def Action(self,obj):
    view_name = "admin:{}_{}_hello".format(obj._meta.app_label, obj._meta.model_name)
    link      = reverse(view_name, args=[obj.pk])
    html      = '<input type="button" onclick="location.href=\'{}\'" value="Delete" />'.format(link)
    return format_html(html)  

  def get_queryset(self, request):
    qs = super().get_queryset(request)
    return qs.filter(lease_status='A')

  def has_change_permission(self, request, obj=None):
    return False

  def has_delete_permission(self, request, obj=None):
    return False
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
    js = (
              '//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js', # jquery
              'registered/js/surrender_lease.js',   # app static folder
          )

    
@admin.register(adjusted_area)        
class adjustedreasAdmin(admin.ModelAdmin):
  form=adjusted_areasForm
  list_display = ('lease_number','Description','Area', 'record_date')
  exclude = ('description',)

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

def hello():
  return 'hello world'

@admin.register(alter_LandUse)        
class alterLandUseAdmin(admin.ModelAdmin):
  form         = alter_landuseForm
  list_display = ('lease_number', 'Description','proposed_land_use','record_date')
  exclude = ('description',)     
  
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


@admin.register(Landuse_Type)        
class LandusechoicesAdmin(admin.ModelAdmin):
  form         = Landuse_choicesForm
  Slist_display = "__all__"     
  ordering = ['landuse']
  
  def has_change_permission(self, request, obj=None):
    return False

  def has_delete_permission(self, request, obj=None):
    return False

  class Media:
    js = ('//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js', # jquery
          'registered/js/landusetype.js',   # app static folder
        )

admin.site.unregister(Group)
