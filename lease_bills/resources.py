from import_export.fields import Field
from registered.models import lease
from reference_tables.models import Landuse_Type
from .models import Bill_payment
from reference_tables.models import reference_table
import datetime
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget, DateWidget
from import_export import resources, fields, widgets
from import_export.widgets import ForeignKeyWidget
from import_export.results import RowResult


class billpaymentResource(resources.ModelResource):
  lease_number = fields.Field(
      column_name='Lease number',
      attribute='lease_number',
      widget=ForeignKeyWidget(lease, field='lease_number')
  )

  class Meta:
    model            = Bill_payment
    fields           = ('payment_date', 'lease_number', 'amount_paid', 'reciept_number')
    exclude          = ('id', 'payment_period')
    import_id_fields = ('lease_number', 'reciept_number')
    skip_unchanged   = True
    report_skipped   = True


              