from django.db import models
from django.db.models import Model
from django import forms
from django.core.validators import  MinLengthValidator,MinValueValidator
from django.db.models import Q
from django.db import connection
from django.core.exceptions import ValidationError
import logging
from datetime import  date
from django.contrib.auth.models import UserManager
logger = logging.getLogger(__name__)
from django.core.validators import  MinLengthValidator,MinValueValidator,MaxValueValidator
import datetime

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
STATE = (
    ('A','Open'),
    ('I','Close'),
)



def year_choices():
    return [(r,r) for r in range(1900, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year
# Create your models here.
class Landuse_Type(Model):
    landuse        = models.CharField(max_length=255,unique=True)
    landuse_code   = models.CharField(max_length=255,unique=True)

    class Meta:
        app_label    = 'reference_tables'
        verbose_name = 'Land use Type'
        verbose_name_plural = 'Land use Types'        

    def __str__(self):
        return self.landuse

class reference_table(Model):

    record_date         = models.DateField(auto_now=True)
    landuse_type        = models.ForeignKey(Landuse_Type,on_delete=models.CASCADE)
    zone_number         = models.PositiveIntegerField (choices=ZONE,default=1)
    period              = models.IntegerField( choices=[(r,r) for r in range(1900, datetime.date.today().year+2)], default=current_year)
    fixed_rate          = models.DecimalField(max_digits=10, decimal_places=3,validators=[MinValueValidator(0.001)])
    penalty             = models.DecimalField(max_digits=5, decimal_places=2,validators=[MinValueValidator(0.01),MaxValueValidator(100)], default=20.23)
    rate_status         = models.CharField(max_length=1,choices=STATUS,default ="A")


    class Meta:
        verbose_name        = 'Ground Rent Rate'
        verbose_name_plural = 'Ground Rent Rates'
        app_label           = "reference_tables"           
        unique_together     = ('zone_number','landuse_type','period')


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
                    cursor.execute ("UPDATE reference_tables_reference_table SET rate_status = %s WHERE  landuse_type_id = %s and zone_number = %s and period <= %s and rate_status = %s",['I',self.landuse_type.id,self.zone_number,self.period,'A'])         
            super(reference_table,self).save(*args,*kwargs)


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
        unique_together     = ('window_number','period')
        verbose_name        = 'Billing Period'
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
                if instance.period_state == 'A':#cloze
                    com = instance.comments
                    cursor.execute("UPDATE reference_tables_billing_period SET closing_date  = %s,period_state=%s, comments =%s  WHERE window_number = %s and period = %s ",[date.today(),'I',com+" [Closing Comments: "+self.comments+"]",instance.window_number,self.period])
                          
                elif  instance.period_state == 'I':#open
                    cursor.execute("INSERT INTO reference_tables_billing_period (record_date,opening_date,period_state,period,window_number,comments,bill_data_set) VALUES (%s,%s,%s,%s,%s,%s,%s)",[date.today(),date.today(),'A',self.period,window_number+1," [ Opening Comments: "+self.comments+" ]",'False'])
            if not saved:
                #open brand new window for billing_period
                cursor.execute("INSERT INTO reference_tables_billing_period (record_date,opening_date,period_state,period,window_number,comments,bill_data_set) VALUES (%s,%s,%s,%s,%s,%s,%s)",[date.today(),date.today(),'A',self.period,window_number+1,"[ Opening Comments: "+self.comments+" ]",'False'])
                
                     
