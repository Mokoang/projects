from django.contrib import admin
from .models import  Bill,Bill_details,Bill_dataset,Bill_payment,Bill_invoice
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.mixins import PermissionRequiredMixin
from reference_tables.models import billing_period
import datetime
from django.utils.html import format_html
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.urls import  path
from registered.models import lease,lease_details
from .forms import invoiceForm
from .resources import billpaymentResource
from django.db import connection
from django.http import HttpResponseRedirect
from django.contrib import messages

class billView(PermissionRequiredMixin, DetailView):
  permission_required = "lease_bills.view_invoice"
  template_name       = "admin/lease_bills/Bill/bill.html"
  model               = Bill

  def get_context_data(self, **kwargs):
    return {
        **super().get_context_data(**kwargs),
        **admin.site.each_context(self.request),
        "opts": self.model._meta,
        "bill_details": Bill_details.objects.filter(status='A').order_by('period'),
        "bill_data"   : Bill_dataset.objects.all(),
      }
   

class invoiceView(PermissionRequiredMixin, DetailView):
  permission_required = "lease_bills.view_invoice"
  template_name       = "admin/lease_bills/Bill_invoice/invoice.html"
  model              = Bill_invoice

  def get_context_data(self, **kwargs):
    billdet_id = self.kwargs.get('pk')
    return {
        **super().get_context_data(**kwargs),
        **admin.site.each_context(self.request),
        "opts": self.model._meta,
        "bill": Bill.objects.all().filter(id=Bill_details.objects.get(id=billdet_id).bill_id_id),
        "bill_id"   : Bill_details.objects.get(id=billdet_id).bill_id_id,
      }


@admin.register(Bill)
class invoiceAdmin(admin.ModelAdmin):
  form = invoiceForm
  list_display       = ['billing_date','lease_number','bill_description','lease_holder','district','Total_bill','Bill_reciept',]
  search_fields      = ['billing_date','lease_number','lease_holder','district']
  search_help_text   = 'Search using lease number,date,lease_holder or district'
  list_per_page      = 10
  list_display_links = None
  
  class Meta:
    model = Bill

  def get_queryset(self, request):
    qs = super().get_queryset(request)

    # Fetching lease numbers with lease_status='A'
    lease_numbers_with_status_a = lease.objects.filter(lease_status='A').values_list('lease_number', flat=True)

    # Filtering bills based on lease numbers with status 'A'
    qs = qs.filter(lease_number__in=lease_numbers_with_status_a)

    return qs

  class Media:
      js = ('//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js', # jquery
              'lease_bills/js/billing_invoice.js',   # app static folder
          )          

  """
  def Bill_reciept(self,obj: Bill)-> str:
    url  = reverse("admin:lease_bills",args=[obj.pk])
    return format_html(f'<a title="invoice" href="{url}">🧾</a>')  
  """ 
  def has_change_permission(self, request, obj=None):
    return False

  def has_delete_permission(self, request, obj=None):
    return False
  Bill_details
  def get_urls(self):
    return [path('<pk>/<lease_number>',  
      self.admin_site.admin_view(billView.as_view()),
      name = f"lease_bills_Bill_lease_number",
      ),*super().get_urls(),]
    
    
  def Bill_reciept(self,obj: Bill)-> str:
    url  = reverse("admin:lease_bills_Bill_lease_number",args=[obj.id,obj.lease_number])
    if obj.bill_status=='Complete':
      return format_html(f'<a title="invoice" href="{url}">🧾</a>')
    else:
      return format_html(f'⛔')
    
  def bill_state(self,obj):
    if obj.bill_status=='Complete':
      return format_html(f'✅')
    else:
      return format_html(f'❌')

  def Total_bill(self,obj):
    total = 0
    for item in Bill_details.objects.filter(bill_id_id = obj.id).filter(status ='A'):
      total +=item.amount_due
      total -=item.amount_paid
  
    return format(total, ".2f")
  
  #saving the bill data in this function...........
  def save_model(self, request, obj, form, change):
      custom_data      =   request.POST.get('custom_data')
      my_array         =   custom_data.split(";") #lease ids...
      array            =   remove_empty_last_element(my_array)
      billing_date     =   form.cleaned_data["billing_date"]
      bill_description =   form.cleaned_data["bill_description"]
      bill_period      =   form.cleaned_data["bill_period"]
      current_date     =   datetime.date.today()
      start_period     =   0


      with connection.cursor() as cursor:
       

        for instance in lease.objects.filter(id__in=array).filter(lease_status ='A'):
          #update or create depending on lease number.....
          cursor.execute("""
          INSERT INTO lease_bills_bill 
          (billing_date,lease_number,bill_description,bill_status,registration_date,lastpayment_date,lease_holder,phone_number,address,district,bill_period_id) 
          VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (lease_number)  DO UPDATE SET 
          billing_date = EXCLUDED.billing_date,bill_description = EXCLUDED.bill_description,bill_status = EXCLUDED.bill_status,registration_date = EXCLUDED.registration_date,lastpayment_date = EXCLUDED.lastpayment_date,lease_holder = EXCLUDED.lease_holder,phone_number = EXCLUDED.phone_number,address = EXCLUDED.address,district = EXCLUDED.district
          """,[billing_date,instance.lease_number,bill_description,'Complete',instance.registration_date,instance.lastpayment_date,instance.lease_holder,instance.phone_number,instance.address,instance.district,bill_period.id])  

          #fetch the id.....
          bill_id            = Bill.objects.get(lease_number = instance.lease_number).id
          lastpayment_period = instance.lastpayment_period
          
          #get total paid for the lease in question
          cursor.execute("SELECT SUM(amount_paid) FROM lease_bills_bill_payment WHERE lease_number_id = %s", [instance.id])
          total_paid_result = cursor.fetchone()
          total_paid = total_paid_result[0] if total_paid_result and total_paid_result[0] is not None else 0
            
          #fetch lease details...
          lease_details_data = []
          results = get_amount_due_per_period(instance.lease_number,bill_period.period)

          if len(str(instance.lastpayment_period))<4:
              start_period=instance.registration_date.year+1
          else:
              start_period =instance.lastpayment_period+1
          
          for data in lease_details.objects.filter(lease_number_id=instance.id).filter(period__gte=start_period).filter(period__lte=bill_period.period).order_by('id'):
            cursor.execute("INSERT INTO testing (name) VALUES (%s) ", ["We here"])
            cursor.execute("INSERT INTO testing (name) VALUES (%s) ", [data.period])    
            cursor.execute("INSERT INTO testing (name) VALUES (%s) ", [instance.lease_number])
            
            #check how much money is paid until this period
            cursor.execute("SELECT SUM(amount_paid) FROM lease_bills_bill_payment WHERE lease_number_id = %s and payment_period = %s", [instance.id,data.period])
            total_paid_result = cursor.fetchone()
            amount_paid       = total_paid_result[0] if total_paid_result and total_paid_result[0] is not None else 0
  

            if len(str(instance.lastpayment_period)) == 4 and data.period > lastpayment_period:
                status = 'A'
            elif data.period > instance.registration_date.year:
                status = 'A'
            else:
                status = 'B'
  
            amount_due         = results['amounts_due'][data.period]
            calculated_penalty = results['penalties'][data.period] 
            lease_details_data.append({
                'bill_id_id': bill_id,
                'period': data.period,
                'bill_description': bill_description,
                'official_area': data.area,
                'area_units': data.area_units,
                'penalty': data.penalty,
                'fixed_rate': data.fixed_rate,
                'landuse_type_id': data.landuse_type_id,
                'zone_number': data.zone_number,
                'status':status,
                'amount_paid':amount_paid,
                'amount_due':amount_due,
                'calculated_penalty':calculated_penalty,
            })

            #Perform bulk insert......
          if lease_details_data:
            cursor.executemany("INSERT INTO lease_bills_bill_details (bill_id_id, period, bill_description, official_area, area_units,penalty, fixed_rate,landuse_type_id, zone_number,status,amount_paid,amount_due,calculated_penalty) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s) ON CONFLICT (bill_id_id,period) DO NOTHING;", [tuple(data.values()) for data in lease_details_data])
        # super().save_model(request, obj, form, change)

def remove_empty_last_element(array):
    if array and array[-1] == "":
        return array[:-1]  # Return array without the last element
    else:
        return array 


  
def get_amount_due_per_period(lease_number, period):
  start_period = 0
  lease_id = 0
  amounts_due = {}
  penalties = {}

  # get lease details for this lease and the starting period
  for data in lease.objects.filter(lease_number=lease_number):
    lease_id = data.id
    if len(str(data.lastpayment_period)) < 4:
      start_period = data.registration_date.year + 1
    else:
      start_period = data.lastpayment_period + 1

  total_balance = 0

  # iterate through periods and calculate amounts and penalties
  for detail in lease_details.objects.filter(lease_number_id=lease_id).filter(period__gte=start_period).filter(period__lte=period):
    ground_rent = detail.fixed_rate * detail.area
    cursor = connection.cursor()

    # get amount paid until the current year
    cursor.execute("SELECT SUM(amount_paid) FROM lease_bills_bill_payment WHERE lease_number_id = %s and payment_period <= %s", [lease_id, detail.period])
    total_paid_result = cursor.fetchone()
    amount_paid = total_paid_result[0] if total_paid_result and total_paid_result[0] is not None else 0

    paid_balance = amount_paid - total_balance
    penalty = 0

    if paid_balance > 0:
        if paid_balance <= ground_rent:
          amount_due_per_period = ground_rent
          penalty = (ground_rent - paid_balance) * (detail.penalty / 100)
        else:
          amount_due_per_period = 0
          penalty = 0
    else:
      penalty = (ground_rent) * detail.penalty / 100
      amount_due_per_period = ground_rent + penalty

    total_balance += (ground_rent + penalty)

    amounts_due[detail.period] = amount_due_per_period
    penalties[detail.period] = penalty

  return {'amounts_due': amounts_due, 'penalties': penalties}
      
def cal_penalty(lease_number,period):
    total_paid      = 0
    total_gr        = 0
    total_pen       = 0
    current_payment = 0
    current_gr      = 0
    curr_pen        = 0
    
    for data in Bill_payment.objects.filter(lease_number = lease.objects.get(lease_number=lease_number).id).filter(payment_period__lte=period):
        total_paid +=data.amount_paid
        if data.payment_period == period:
            current_payment +=data.amount_paid

    for thedata in Bill_details.objects.filter(bill_id=Bill.objects.get(lease_number=lease_number).id).filter(period__lte=period):
        total_gr        += (thedata.official_area*thedata.fixed_rate)
        
        if thedata.period == period:
            current_gr  = thedata.official_area*thedata.fixed_rate
        if total_paid == 0:
            total_pen +=  thedata.official_area*thedata.fixed_rate*thedata.penalty/100
            curr_pen   = thedata.official_area*thedata.fixed_rate*thedata.penalty/100
        else:
            total_grpen = total_gr+total_pen-current_gr
            totalbal    = total_paid - total_grpen

            if totalbal>0:
                total = totalbal-current_gr
                if total < 0:
                    curr_pen = -1*total*thedata.penalty/100
            else:
                curr_pen = thedata.official_area*thedata.fixed_rate*thedata.penalty/100       
    return  round(curr_pen, 2)

def gettotalgroundrent(lease_number,start_period,end_period):
   total_ground_rent = 0
  

   return total_ground_rent                

def get_totalpaid(lease_number):
    total = 0
    for data in Bill_payment.objects.filter(lease_number = lease.objects.get(lease_number=lease_number).id):
        total +=data.amount_paid
    return total
 

    # ground_rent = 0
    # penalty     = 0
    # t_penalty   = 0
    # t_paid      = 0     
    # for data in Bill_details.objects.filter(bill_id=obj.id):
    #   ground_rent+=(data.fixed_rate*data.official_area) 
    #   penalty    = data.penalty*(data.fixed_rate*data.official_area)/100
    #   paid=0
    #   for pay_data in Bill_payment.objects.filter(lease_number__lease_number=obj.lease_number).filter(payment_period = data.period):
    #     paid+=pay_data.amount_paid
    #   if paid>0:
    #     t_paid     +=paid
    #   else:
    #     if date.today().year>data.period:
    #       t_penalty  +=penalty
    # return 'M '+format(ground_rent+t_penalty-t_paid, ".2f")     


  # def latest_bill_period(self,obj):
  #   return obj.window_period.period

def get_super(x):
  normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
  super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
  res = x.maketrans(''.join(normal), ''.join(super_s))
  return x.translate(res)


@admin.register(Bill_payment)
class BillPaymentAdim(ImportExportModelAdmin,admin.ModelAdmin):
  list_display       = ['payment_date','lease_number','amountpaid','reciept_number','invoice_number']
  search_fields      = ['lease_number']
  fields             = ('payment_date','lease_number','amount_paid','reciept_number','invoice_number')
  search_help_text   = 'Search using lease number'
  list_per_page      = 10
  list_display_links = None
  resource_class     = billpaymentResource

  class Meta:
    model = Bill_payment

  def amountpaid(self,obj):
    return'M '+str(obj.amount_paid)

  def get_queryset(self, request):
    qs = super().get_queryset(request)

    # Joining the lease model with lease_details using ForeignKey
    qs = qs.filter(lease_number__lease_status='A')

    return qs 

  def has_change_permission(self, request, obj=None):
    return False

  def has_delete_permission(self, request, obj=None):
    return False

  class Media:
    js = ('//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js', 'registered/js/bill_payment.js',) 


    
from django.shortcuts import render
# @admin.register(Bill_dataset)  
# class bdAdmin(ExtraButtonsMixin,admin.ModelAdmin):
#   change_form_template = 'admin/lease_bills/bill_dataset/custom_change_form.html'
#   actions              = ['delete_selected']
#   list_display         = ('lease_number','registration_date','lastpayment_date','lastpayment_period','lease_holder','phone_number','district','send_for_bill')
#   form                 = billDatasetForm 

#   def get_queryset(self, request):
#       # Get the original queryset using the parent class method
#       queryset = super(bdAdmin, self).get_queryset(request)
#       # Filter the queryset to include only instances where send_for_bill is True
#       queryset = queryset.filter(send_for_bill=True)
#       return queryset
      
#   def has_change_permission(self, request, obj=None):
#     return False

#   def has_delete_permission(self, request, obj=None):
#     return False
  
  # def has_add_permission(self, request, obj=None):
  #   thestate = False
  #   for thedata in billing_period.objects.all().order_by("-id")[:1]:
  #     if thedata.period_state == 'A':
  #       thestate = True
  #   return thestate  
  # admin.py
  # def delete_selected(self, request, queryset):
  #   queryset.update(data_state='D')
  #   for instance in Bill_dataset.objects.all().filter(data_state='D'):
  #     connection.cursor().execute("UPDATE registered_lease SET send_for_bill = %s WHERE lease_number = %s",[False,instance.lease_number])
  #     connection.cursor().execute("Delete FROM lease_bills_bill_dataset WHERE lease_number = %s",[instance.lease_number])


  # # def get_actions(self, request):
  #   actions = super(bdAdmin, self).get_actions(request)
  #   for data in billing_period.objects.all().order_by('-id')[:1]:
  #     if data.period_state=='I':
  #       del actions['delete_selected']
  #   return actions
  # #units
  # def Area(self,obj):
  #   final_units = f'{obj.area} {obj.area_units}'
  #   if(obj.area_units=='sq_m'):
  #     final_units =f'{obj.area} m\N{SUPERSCRIPT TWO}'id_custom_data
  #   return final_units

  # def get_queryset(self, request):
  #   qs = super().get_queryset(request)
  #   return qs.filter(data_state='P')

  # myapp/admin.py
  # class Media:
  #   js = ('//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js', # jquery
  #           'lease_bills/js/bill_dataset.js',   # app static folder
  #       )

        
  # def save_model(self, request, obj, form, change):
  #     # Call the parent method to save the object normally
  #     #super().save_model(request, obj, form, change)

  #     # Retrieve the custom data from the request.POST dictionary
  #     custom_data = request.POST.get('custom_data')
  #     array       = custom_data.split(";")
       

  #     with connection.cursor() as cursor:
  #       verperid = 0
  #       for thedata in billing_period.objects.all().order_by("-id")[:1]:
  #         verperid = thedata.id
  #       for i in array[:len(array)-1]:
  #         for instance in lease.objects.filter(id=int(i)):
  #           #this is the loop where you can lease bills whose data has not changed through out all the years..
  #           connection.cursor().execute("UPDATE registered_lease SET send_for_bill =  %s WHERE id = %s",[True,i])  
  #     # Perform any custom logic with the data, e.g. store it in a separate model or database
  #     # In this example, we will just update the object's custom_data field
  #     obj.custom_data = custom_data
  #     #obj.save()    

@admin.register(Bill_invoice)        
class billinvoiceAdmin(admin.ModelAdmin):
   
   list_display       = ['get_lease_number','lease_holder','District','period','invoice_reciept']
   search_fields      = ['bill_id__lease_number','bill_id__lease_holder','bill_id__district']
   search_help_text   = 'Search using lease number,date,lease_holder or district'
   list_per_page      = 10
   list_display_links = None


   def get_lease_number(self,obj):
      return Bill.objects.get(id=obj.bill_id_id).lease_number
   
   get_lease_number.short_description = 'Lease Number' 

   list_select_related = ('bill_id', )

   def get_urls(self):
    return [path('<pk>/',  
      self.admin_site.admin_view(invoiceView.as_view()),
      name = f"lease_bills_Bill_invoice_lease_number",
      ),*super().get_urls(),]
    

   def invoice_reciept(self,obj: Bill)-> str:
      url  = reverse("admin:lease_bills_Bill_invoice_lease_number",args=[obj.pk])
      return format_html(f'<a title="invoice" href="{url}">🧾</a>')
   
   def has_change_permission(self, request, obj=None):
      return False

   def has_delete_permission(self, request, obj=None):
      return False

   def has_add_permission(self, request, obj=None):
      return False
   

   def lease_holder(self,obj):
      return Bill.objects.get(id=obj.bill_id_id).lease_holder 
    

   def District(self,obj):
      return Bill.objects.get(id=obj.bill_id_id).district
   
# @admin.register(billdata)        
# class billdataAdmin(admin.ModelAdmin):
#   actions = ['send_for_billing']
#   #readonly_fields = ['area_units',]       
#   list_display = ('registration_date','lastpayment_date','lastpayment_period','lease_number','landuse_type', 'zone_number','Area','status')
#   #list_filter = ("lease_status", )
#   #exclude = ('lease_status',)
#   #search_fields = ['registration_date','lastpayment_date','lastpayment_period','lease_number','landuse_type__landuse', 'zone_number','area',]
#   list_per_page = 10

#   def registration_date(self,obj):
#       return list(lease.objects.all())
#   #units
#   def Area(self,obj):
#     final_units = f'{obj.area} {obj.area_units}'
#     if(obj.area_units=='sq_m'):
#       final_units =f'{obj.area} m\N{SUPERSCRIPT TWO}'
#     return final_units
#   #status
#   def status(self,obj):
#     if obj.lease_status=='A':   
#         return True
#     return False   
    
#   status.boolean = True
#   def has_change_permission(self, request, obj=None):
#     return False

#   def has_delete_permission(self, request, obj=None):
#     return False
  
#   def has_add_permission(self, request, obj=billing_period.objects.all()):
#     return False
  
#   def send_for_billing(self, request, queryset):
#     verperid = 0

#     for thedata in billing_period.objects.all().order_by("-id")[:1]:
#       verperid = thedata.id
#     for instance in queryset:
#       connection.cursor().execute("UPDATE  lease_bills_billdata SET billdata =  %s WHERE lease_number = %s",[True,instance.lease_number])  
#       connection.cursor().execute("INSERT INTO lease_bills_Bill_dataset (record_date,lease_number,zone_number,lastpayment_period,registration_date,lastpayment_date,window_period_id,landuse_type_id,area,area_units,data_state) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[date.today(),instance.lease_number,instance.zone_number,instance.lastpayment_period,instance.registration_date,instance.lastpayment_date,verperid,instance.landuse_type_id,instance.area,instance.area_units,'P'])
#     #send for billing

#   def get_queryset(self, request):
#     qs = super().get_queryset(request)
#     return qs.filter(billdata=False).filter(lease_status='A')
#   def get_actions(self, request):
#     actions = super(billdataAdmin, self).get_actions(request)
#     present = False
#     for data in billing_period.objects.all().order_by('-id')[:1]:
#       present = True
#       if data.period_state=='I':
#         del actions['send_for_billing']
#     if not present:
#       del actions['send_for_billing']

#     return actions
 