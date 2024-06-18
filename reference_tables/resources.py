from import_export.fields import Field
from registered.models import lease
from reference_tables.models import Landuse_Type
from reference_tables.models import reference_table
import datetime
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget, DateWidget


#This class is used to define the import / export functions
class rtAdminResource(resources.ModelResource):
  landuse_type        = Field(column_name='Land-use Type',attribute='landuse_type', widget=ForeignKeyWidget(Landuse_Type, field='landuse_code')) 
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