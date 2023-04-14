from import_export.fields import Field
from .models import lease, surrendered_lease,adjusted_area,alter_LandUse,Landuse_Type
import datetime
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget, DateWidget



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
    landus = instance.landuse_type.landuse
    for instance2 in Landuse_Type.objects.all():
      if  landus == instance2.landuse:
        found = True

    if not found:
      skip = True

    #check Date.......
  
    if(str(instance.registration_date) != datetime.datetime.strptime(str(instance.registration_date), '%Y-%m-%d').strftime('%Y-%m-%d')) :
      skip = True

    if(str(instance.lastpayment_date )!= datetime.datetime.strptime(str(instance.lastpayment_date), '%Y-%m-%d').strftime('%Y-%m-%d')) :
      skip = False     
    return skip


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



class adjustareaAdminResource(resources.ModelResource):

  record_date    = Field(attribute='record_date', column_name = 'Record date', widget = DateWidget("%d/%m/%Y"))
  comments       = Field(attribute='comments', column_name = 'Comments')
  lease_number   = Field(column_name='Lease number', attribute='lease_number', widget=ForeignKeyWidget(lease, field='lease_number'))
  proposed_area  = Field(column_name='Area', attribute='proposed_area')
  area_units     = Field(column_name='Units',attribute='area_units') 

  class Meta:
    model            = adjusted_area
    fileds           = ('record_date','lease_number','proposed_area','area_units','comments')
    export_order     = ('record_date','lease_number','proposed_area','area_units','comments')
    exclude          = ('id','description',)
    import_id_fields = ('lease_number','proposed_area','area_units','record_date')
    skip_unchanged    = True
    report_skipped    = True  
  

class alterlanduseAdminResource(resources.ModelResource):

  record_date       = Field(attribute='record_date', column_name = 'Record date', widget = DateWidget("%d/%m/%Y"))
  lease_number      = Field(column_name='Lease number', attribute='lease_number', widget=ForeignKeyWidget(lease, field='lease_number'))
  comments          = Field(attribute='comments', column_name = 'Comments')
  proposed_land_use = Field(column_name='Proposed Landuse', attribute='proposed_land_use', widget=ForeignKeyWidget(Landuse_Type, field='landuse'))
  


  def after_save_instance(self, instance, using_transactions, dry_run):
    # the model instance will have been saved at this point, and will have a pk
    print(instance.pk)


  class Meta:
    model            = alter_LandUse
    fileds           = ('record_date','lease_number','proposed_land_use','comments')
    export_order     = ('record_date','lease_number','proposed_land_use','comments')
    exclude          = ('id','description',)
    import_id_fields = ('lease_number','proposed_land_use','record_date')
    skip_unchanged    = True
    report_skipped    = True    
    



