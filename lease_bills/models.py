from django.db import models
from django.db.models import Model
from django import forms
from django.core.validators import  MinLengthValidator,MinValueValidator,MaxValueValidator
from django.db.models import Q
from django.db import connection
from django.core.exceptions import ValidationError
from registered.models import Landuse_Type,lease,alter_LandUse,adjusted_area
import logging
from datetime import  date

logger = logging.getLogger(__name__)
# Create your models here.
#Lease details

ZONE = (
    (1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5),
    (6,6),
)
STATUS = (
    ('A','Active'),
    ('I','Inactive'),
)

import datetime

def year_choices():
    return [(r,r) for r in range(1900, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year

STATE = (
    ('A','Open'),
    ('I','Close'),
)
class billing_period(Model):
    record_date     = models.DateField(auto_now=True)
    opening_date    = models.DateField(auto_now = False,default=date.today)
    closing_date    = models.DateField(auto_now = False,default=date.today,null=True,blank=True)
    period_state    = models.CharField(max_length=1,choices=STATE,default ="A")
    period          = models.IntegerField( choices=[(r,r) for r in range(1900, datetime.date.today().year+2)], default=current_year)
    window_number   = models.IntegerField(default=1)
    bill_data_set   = models.BooleanField(default=False)
    comments        = models.CharField(max_length=255,default='Valid')
    
    class Meta:
        unique_together = ('window_number','period')
        verbose_name = 'Billing Period'
        verbose_name_plural = 'Billing Periods' 


    def __str__(self):
        return str(self.period)+'-'+str(self.window_number)
     
    def save(self,*args,**kwargs):
        with connection.cursor() as cursor:
            saved = False
            closed = False
            open = True
            window_number = 0
            for instance in billing_period.objects.all().filter(period = self.period).order_by("-id")[:1]:
                saved = True
                window_number = instance.window_number
                if instance.period_state == 'A':
                    #close the period
                    com = instance.comments
                    cursor.execute("UPDATE lease_bills_billing_period SET closing_date  = %s,period_state=%s, comments =%s  WHERE window_number = %s and period = %s ",[date.today(),'I',com+" [Closing Comments: "+self.comments+"]",instance.window_number,self.period])
                    cursor.execute("UPDATE lease_bills_bill_dataset SET data_state = %s where data_state = %s",['C','P'])
                    
                elif  instance.period_state == 'I':
                    #open another window in this period
                    cursor.execute("INSERT INTO lease_bills_billing_period (record_date,opening_date,period_state,period,window_number,comments) VALUES (%s,%s,%s,%s,%s,%s)",[date.today(),date.today(),'A',self.period,window_number+1," [ Opening Comments: "+self.comments+" ]"])
                    cursor.execute("UPDATE lease_bills_billdata SET billdata = %s WHERE billdata = %s and lease_status = %s ",[False,True,'A'])
            if not saved:
                #open brand new window for billing_period
                cursor.execute("INSERT INTO lease_bills_billing_period (record_date,opening_date,period_state,period,window_number,comments,bill_data_set) VALUES (%s,%s,%s,%s,%s,%s,%s)",[date.today(),date.today(),'A',self.period,window_number+1,"[ Opening Comments: "+self.comments+" ]",False])
                cursor.execute("UPDATE lease_bills_billdata SET billdata = %s WHERE billdata = %s and lease_status = %s ",[False,True,'A'])
                
             

UNITS=(
    (f'm\N{SUPERSCRIPT TWO}',f'm\N{SUPERSCRIPT TWO}'),
  
)

ZONE = (
    (1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5),
    (6,6),
)

STATES = (
    ('P','Pre-commit'),
    ('C','Commit'),
    ('D','Deleted'),
    )

class Bill_dataset(Model):

    record_date         = models.DateField(auto_now=True)
    lease_number        = models.TextField(max_length=50,name="lease_number",validators=[MinLengthValidator(7)],blank=True)
    area                = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.01)],blank=True)
    area_units          = models.CharField(max_length=50,default='m\N{SUPERSCRIPT TWO}',blank=True)
    landuse_type        = models.ForeignKey(Landuse_Type,on_delete=models.CASCADE,blank=True)    
    zone_number         = models.PositiveIntegerField (choices=ZONE,default=1,blank=True)
    lastpayment_period  = models.IntegerField( choices=[(r,r) for r in range(1900, datetime.date.today().year+1)], blank=True,default=0,null=True) 
    registration_date   = models.DateField(auto_now = False,default=date.today,blank=True)
    lastpayment_date    = models.DateField(blank=True,null=True)
    window_period       = models.ForeignKey(billing_period,on_delete=models.CASCADE,limit_choices_to=Q(bill_data_set=True),blank=True)
    data_state          = models.CharField(max_length=1,choices=STATES,default ="P",blank=True)

    class Meta:
        verbose_name        = 'Billing Data'
        verbose_name_plural = 'Billing Data'
        unique_together     = ('lease_number','window_period') 

    def save(self,*args,**kwargs):
        with connection.cursor() as cursor:
            cursor.execute ("INSERT INTO testing (name) VALUES (%s)",['I did it'])         
            



class reference_table(Model):

    record_date         = models.DateField(auto_now=True)
    landuse_type        = models.ForeignKey(Landuse_Type,on_delete=models.CASCADE)
    zone_number         = models.PositiveIntegerField (choices=ZONE,default=1)
    period              = models.IntegerField( choices=[(r,r) for r in range(1900, datetime.date.today().year+2)], default=current_year)
    fixed_rate          = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.01)])
    penalty             = models.DecimalField(max_digits=4, decimal_places=2,validators=[MinValueValidator(0.01),MaxValueValidator(100)], default=20.23)
    rate_status         = models.CharField(max_length=1,choices=STATUS,default ="A")

    class Meta:
        verbose_name = 'Reference Table'
        verbose_name_plural = 'Reference Tables'
        app_label  = "lease_bills"           
        unique_together = ('zone_number','landuse_type','period')


    def save(self,*args,**kwargs):
        with connection.cursor() as cursor:
            lessthan = False
            for instance in reference_table.objects.filter(landuse_type = self.landuse_type):

                if(instance.period > self.period):
                    lessthan = True

                if lessthan:
                    self.rate_status = 'I'
                    #input with status set to I
                    
                # if for a land type recorded with similar zone number but financial year is less mthan current and price status is still active alter the status to I
                else:
                    cursor.execute ("UPDATE lease_bills_reference_table SET rate_status = %s WHERE  landuse_type_id = %s and zone_number = %s and period <= %s and rate_status = %s",['I',self.landuse_type.id,self.zone_number,self.period,'A'])         
            super(reference_table,self).save(*args,*kwargs)

class Bill(Model):
    billing_date        = models.DateField(auto_now=False,default=date.today)
    lease_number        = models.TextField(max_length=50,unique=True,name="lease_number",validators=[MinLengthValidator(7)])
    bill_description    = models.CharField(max_length=255)
    window_period       = models.ForeignKey(billing_period,on_delete=models.CASCADE,limit_choices_to=Q(period_state='I'))
       

    class Meta:
        verbose_name = 'Lease Bill'
        verbose_name_plural = 'Lease Bills'   
    

    def save(self,*args,**kwargs):
        with connection.cursor() as cursor:
            for instance in Bill_dataset.objects.all().filter(window_period=self.window_period).filter(data_state='C'):
                #Get start and finish periods...
                if instance.lastpayment_period !=None:
                    if instance.lastpayment_period<self.billing_date.year: 
          
                        for reference_data in reference_table.objects.all().filter(landuse_type=instance.landuse_type).filter(zone_number=instance.zone_number).filter(period=instance.window_period.period):
                            cursor = connection.cursor()
                            cursor.execute("select nextval('invoicenumber') ")

                            order_number = cursor.fetchone()

                            today = datetime.date.today()
                            year = u'%4s' % today.year
                            month = u'%02i' % today.month
                            day = u'%02i' % today.day

                            new_number = u'%06i' % order_number
                            newresult =  "INV-"+year+month+day+new_number

                            total_amt = reference_data.fixed_rate*instance.area
                            if self.window_period.period < self.billing_date.year:
                                total_amt =(100+reference_data.penalty)*total_amt/100                    

                            found = False  
                            bill_id = 0                    
                            for thedata in Bill.objects.all().filter(lease_number = instance.lease_number)[:1]:
                                bill_id  = thedata.id
                                found=True

                            if not found:    
                                cursor.execute("INSERT INTO lease_bills_bill (billing_date,lease_number,window_period_id,bill_description) VALUES (%s,%s,%s,%s)",[self.billing_date,instance.lease_number,self.window_period_id,self.bill_description])
                            
                            for adata in Bill.objects.all().filter(lease_number = instance.lease_number)[:1]:
                                bill_id = adata.id

                            detfound = False        
                            for detdata in Bill_details.objects.all().filter(bill_id=bill_id).filter(window_period = self.window_period):
                                detfound = True
                            cursor.execute("INSERT INTO testing (name) VALUES (%s)",["1 = "+str(bill_id)])    
                            if not detfound:                           
                                cursor.execute("INSERT INTO lease_bills_bill_details (bill_id_id,window_period_id,bill_description,official_area ,area_units, penalty ,fixed_rate ,amount,landuse_type_id,zone_number) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[bill_id,instance.window_period.id,self.bill_description,instance.area,instance.area_units,reference_data.penalty,reference_data.fixed_rate,total_amt,instance.landuse_type_id,instance.zone_number])  
                else:
                    for reference_data in reference_table.objects.all().filter(landuse_type=instance.landuse_type).filter(zone_number=instance.zone_number).filter(period=instance.window_period.period):

                                            
                        cursor = connection.cursor()
                        cursor.execute("select nextval('invoicenumber') ")

                        order_number = cursor.fetchone()

                        today = datetime.date.today()
                        year = u'%4s' % today.year
                        month = u'%02i' % today.month
                        day = u'%02i' % today.day

                        new_number = u'%06i' % order_number
                        newresult =  "INV-"+year+month+day+new_number


                        total_amt = reference_data.fixed_rate*instance.area
                        if self.window_period.period < self.billing_date.year:
                            total_amt =(100+reference_data.penalty)*total_amt/100

                        found = False  
                        bill_id = 0                    
                        for thedata in Bill.objects.all().filter(lease_number = instance.lease_number)[:1]:
                            found=True
                        if not found:    
                            cursor.execute("INSERT INTO lease_bills_bill (billing_date,lease_number,window_period_id,bill_description) VALUES (%s,%s,%s,%s)",[self.billing_date,instance.lease_number,self.window_period_id,self.bill_description])
                        
                        for bdata in Bill.objects.all().filter(lease_number = instance.lease_number)[:1]:
                            bill_id = bdata.id

                        detfound = False        
                        for detdata in Bill_details.objects.all().filter(bill_id=bill_id).filter(window_period = self.window_period):
                            detfound = True


                        cursor.execute("INSERT INTO testing (name) VALUES (%s)",["2 = "+str(bill_id)])  
                        if not detfound:                           
                            cursor.execute("INSERT INTO lease_bills_bill_details (bill_id_id,window_period_id,bill_description,official_area ,area_units, penalty ,fixed_rate ,amount,landuse_type_id,zone_number) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[bill_id,instance.window_period_id,self.bill_description,instance.area,instance.area_units,reference_data.penalty,reference_data.fixed_rate,total_amt,instance.landuse_type_id,instance.zone_number])  

#billing detail              
class Bill_details(Model):
    
    bill_id             = models.ForeignKey(Bill,on_delete=models.CASCADE)
    window_period       = models.ForeignKey(billing_period,on_delete=models.CASCADE,limit_choices_to=Q(period_state='I'))
    bill_description    = models.CharField(max_length=255)
    official_area       = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.00)])
    area_units          = models.CharField(max_length=255)
    landuse_type        = models.ForeignKey(Landuse_Type,on_delete=models.CASCADE)
    penalty             = models.DecimalField(max_digits=4, decimal_places=2,validators=[MinValueValidator(0.01),MaxValueValidator(100)])
    fixed_rate          = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.00)])
    amount              = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.00)])
    zone_number         = models.PositiveIntegerField (choices=ZONE,default=1)

    class Meta:
        unique_together = ('bill_id','window_period')
    
    


class billdata(Model):
    lease_number        = models.TextField(max_length=50,unique=True,name="lease_number",validators=[MinLengthValidator(7)])
    zone_number         = models.PositiveIntegerField (choices=ZONE,default=1)
    area                = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.01)])
    area_units          = models.CharField(max_length=50,default='m\N{SUPERSCRIPT TWO}')
    landuse_type        = models.ForeignKey(Landuse_Type,on_delete=models.CASCADE) 
    lease_status        = models.CharField(max_length=1,choices=STATUS,default ="A")
    lastpayment_period  = models.IntegerField( choices=[(r,r) for r in range(1900, datetime.date.today().year+1)], blank=True,default=0,null=True) 
    registration_date   = models.DateField(auto_now = False,default=date.today)
    lastpayment_date    = models.DateField(blank=True,null=True)
    billdata            = models.BooleanField(default=False)

    def __str__(self):
        return self.lease_number

    class Meta:
        verbose_name = 'Data Bucket'
        verbose_name_plural = 'Data Bucket' 


  
 