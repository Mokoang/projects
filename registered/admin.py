from django.contrib import admin
from .models import lease, surrendered_lease,adjusted_area,alter_LandUse,Landuse_Type
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
from lease_bills.models import reference_table,verification,correction
import re
from datetime import  date
from django.utils.html import format_html
from django.urls import reverse
from django.urls import include, path
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.admin.templatetags import admin_modify
from .forms import leaseForm, surrendered_leaseForm,alter_landuseForm,Landuse_choicesForm,adjusted_areasForm
from .resources import LeaseAdminResource,slAdminResource,adjustareaAdminResource,alterlanduseAdminResource


submit_row = admin_modify.submit_row
def submit_row_custom(context):
    ctx = submit_row(context)
    ctx['show_save_and_add_another'] = False
    ctx['show_save_and_continue'] = False
    return ctx
admin_modify.submit_row = submit_row_custom


@admin.register(lease)        
class leaseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
  form=leaseForm
  actions = ['send_for_billing']
  fields =   ['lease_number', 'landuse_type',('area','area_units'),'zone_number','registration_date','lastpayment_date','lastpayment_period']
  readonly_fields = ['area_units',]       
  list_display = ('registration_date','lastpayment_date','lastpayment_period','lease_number','landuse_type', 'zone_number','Area','status')
  resource_class = LeaseAdminResource
  exclude = ('lease_status',)
  search_fields = ['registration_date','lastpayment_date','lastpayment_period','lease_number','landuse_type__landuse', 'zone_number','area',]
  list_per_page = 10

  class Meta:
    model = lease

  def corrected(self,obj):
    return obj.correction_state
  corrected.boolean = True


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
  
  def send_for_billing(self, request, queryset):
    lease.objects.update(billdata = False)
    queryset.update(billdata=True)
    #send for bill data....
    connection.cursor().execute("UPDATE lease_bills_verification SET bill_dataset = True Where id = (SELECT id FROM lease_bills_verification ORDER BY id DESC LIMIT 1);",[date.today().year])

    for instance in lease.objects.all().filter(billdata = True):
      connection.cursor().execute("INSERT INTO lease_bills_Bill_dataset (record_date,lease_number,zone_number,lastpayment_period,registration_date,lastpayment_date) VALUES (%s,%s,%s,%s,%s,%s)",[date.today(),instance.lease_number,instance.zone_number,instance.lastpayment_period,instance.registration_date,instance.lastpayment_date])


      thearea_list      = []
      theareaunit_list  = []
      therecorddate_list= []

      for area_data in adjusted_area.objects.all().filter(lease_number_id = instance.id).order_by('record_date'):
          if(len(thearea_list)>0):
              # insertion 2,3,4,5 etc
              #check same year changes
              if(therecorddate_list[len(thearea_list)-1].year==area_data.record_date.year):
                  #check the date that is below the closing date

                  if (therecorddate_list[len(thearea_list)-1] <= area_data.record_date and area_data.record_date<=self.billing_date):
                      thearea_list[len(thearea_list)-1]=area_data.proposed_area
                      theareaunit_list[len(thearea_list)-1]=instance.area_units
                      therecorddate_list[len(therecorddate_list)-1]=area_data.record_date
              else:#diffrent year changes
                  thearea_list.append(area_data.proposed_area)
                  theareaunit_list.append(instance.area_units)
                  therecorddate_list.append(area_data.record_date)

          else:#initial insertio
              if area_data.description=='Initial':
                  thearea_list.append(area_data.proposed_area)
                  theareaunit_list.append(instance.area_units)
                  therecorddate_list.append(area_data.record_date)
              else:#description is another thing else
                  thearea_list.append(area_data.proposed_area)
                  theareaunit_list.append(instance.area_units)
                  therecorddate_list.append(area_data.record_date) 
      if len(thearea_list)==0:
          thearea_list.append(instance.area)
          theareaunit_list.append(instance.area_units)
          therecorddate_list.append(instance.registration_date)

      landusetype_list = []
      recorddate_list  = []
      

      for landuse_data in alter_LandUse.objects.all().filter(lease_number_id = instance.id).order_by('record_date'):
          if(len(landusetype_list)>0):# insertion 2,3,4,5 etc
              #check same year changes
              
              if(recorddate_list[len(landusetype_list)-1].year==landuse_data.record_date.year):
                  
                  #check the date that is below the closing date
                  if (recorddate_list[len(landusetype_list)-1] <= landuse_data.record_date and landuse_data.record_date<=self.billing_date ):
                      landusetype_list[len(landusetype_list)-1]=landuse_data.proposed_land_use_id
                      recorddate_list[len(recorddate_list)-1]=landuse_data.record_date
              else:#diffrent year changes
                  landusetype_list.append(landuse_data.proposed_land_use_id)
                  recorddate_list.append(landuse_data.record_date)

          else:#initial insertio
              if landuse_data.description=='Initial':
                  landusetype_list.append(landuse_data.proposed_land_use_id)
                  recorddate_list.append(landuse_data.record_date)
              else:#description is another thing else
                  landusetype_list.append(landuse_data.proposed_land_use_id)
                  recorddate_list.append(landuse_data.record_date) 

      if len(landusetype_list)==0:
          landusetype_list.append(instance.landuse_type_id)
          recorddate_list.append(instance.registration_date)
        
          
      for i in range(len(thearea_list)):
          #connection.cursor().execute("INSERT INTO lease_bills_billdata_area (lease_number_id,area,units,period) VALUES (%s,%s,%s,%s)",[instance.id,thearea_list[i],theareaunit_list[i],therecorddate_list[i].year])    
          connection.cursor().execute("INSERT INTO testing (name,description) VALUES (%s,%s)",[thearea_list[i],therecorddate_list[i].year])    
     
      for i in range(len(landusetype_list)):
          connection.cursor().execute("INSERT INTO lease_bills_billdata_Landuse (lease_number_id,landuse_id,period) VALUES (%s,%s,%s)",[instance.id,landusetype_list[i],recorddate_list[i].year])    


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
    

  def has_add_permission(self, request, obj=verification.objects.all()):
    has_permission  = True
    for data in verification.objects.all():
      if data.period == date.today().year and data.bill_dataset==False : #verified
        has_permission = False
    return has_permission
  

  def has_import_permission(self, request, obj=None):
    has_permission  = True
    for data in verification.objects.all():
      if data.period == date.today().year and data.bill_dataset==False : #verified
        has_permission = False
    return has_permission

  def has_export_permission(self, request, obj=None):
    has_permission  = True
    for data in verification.objects.all():
      if data.period == date.today().year and data.bill_dataset==False : #verified
        has_permission = False
    return has_permission

  """
  def get_actions(self, request):
    actions = super(leaseAdmin, self).get_actions(request)
    for data in verification.objects.all():
      if data.period == date.today().year :
        del actions['Validate']
    return actions
  """
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

  def has_add_permission(self, request, obj=None):
    has_permission  = True
    for data in verification.objects.all():
      if data.period == date.today().year : #verified
        has_permission = False
    if has_permission:#not yet verified
      connection.cursor().execute('UPDATE registered_lease SET verified = False')
    return has_permission


  def has_import_permission(self, request, obj=None):
    has_permission  = True
    for data in verification.objects.all():
      if data.period == date.today().year :
        has_permission = False
    return has_permission         

    
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


#----------------------------------------------------------------------------------
  def has_add_permission(self, request, obj=verification.objects.all()):
    has_permission  = True
    for data in verification.objects.all():
      if data.period == date.today().year : #verified
        has_permission = False
      if not has_permission:
        #check correction......
        for cdata in correction.objects.all().order_by('-period').order_by('-id')[:1]:
          if  cdata.period == date.today().year:
            if cdata.correction_status=='I':
              has_permission = False
            elif cdata.correction_status=='A':
              has_permission = True 
          else:
            #no open correction
            has_permission = False
    return has_permission


  def has_import_permission(self, request, obj=None):
    has_permission  = True
    for data in verification.objects.all():
      if data.period == date.today().year :
        has_permission = False
      else:
        #check correction......
        for cdata in correction.objects.all().order_by('-period').order_by('-id')[:1]:
          if  cdata.period == date.today().year:
            if cdata.correction_status=='I':
              has_permission = False
            elif cdata.correction_status=='A':
              has_permission = True 
          else:
            #no open correction
            has_permission = False
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

#----------------------------------------------------------------------------------
  def has_add_permission(self, request, obj=verification.objects.all()):
    has_permission  = True
    for data in verification.objects.all():
      if data.period == date.today().year : #verified
        has_permission = False
      if not has_permission:
        #check correction......
        for cdata in correction.objects.all().order_by('-period').order_by('-id')[:1]:
          if  cdata.period == date.today().year:
            if cdata.correction_status=='I':
              has_permission = False
            elif cdata.correction_status=='A':
              has_permission = True 
          else:
            #no open correction
            has_permission = False
    return has_permission


  def has_import_permission(self, request, obj=None):
    has_permission  = True
    for data in verification.objects.all():
      if data.period == date.today().year :
        has_permission = False
      else:
        #check correction......
        for cdata in correction.objects.all().order_by('-period').order_by('-id')[:1]:
          if  cdata.period == date.today().year:
            if cdata.correction_status=='I':
              has_permission = False
            elif cdata.correction_status=='A':
              has_permission = True 
          else:
            #no open correction
            has_permission = False
    return has_permission



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
