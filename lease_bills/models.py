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
    
    lease_number        = models.ForeignKey(lease,on_delete=models.CASCADE)
    billing_date        = models.DateField(auto_now=False,default=date.today)
    invoice_number      = models.CharField(max_length=255)
    bill_description    = models.CharField(max_length=255)       
    balance             = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.01)])

     
    def __str__(self):
        return self.invoice_number


    class Meta:
        verbose_name = 'Lease Bill'
        verbose_name_plural = 'Lease Bills'   
        unique_together = ('lease_number','billing_date')
    

    def save(self,*args,**kwargs):
        with connection.cursor() as cursor:

            for instance in lease.objects.all().filter(lease_status = 'A'):

             


                thearea_list      = []
                theareaunit_list  = []
                therecorddate_list= []

                for area_data in adjusted_area.objects.all().filter(lease_number_id = instance.id).order_by('record_date'):
                    if(len(thearea_list)>0):# insertion 2,3,4,5 etc
                        #check same year changes
                        
                        if(therecorddate_list[len(thearea_list)-1].year==area_data.record_date.year):
                            
                            #check the date that is below the closing date
                            closingdate = False
                            for closingdata in Bill_finale.objects.all().filter(period = area_data.record_date.year):
                                closingdate = True
                                if area_data.record_date <=closingdata.closing_date:                
                                    if (therecorddate_list[len(thearea_list)-1] <=area_data.record_date and area_data.record_date<=self.billing_date ):
                                        thearea_list[len(thearea_list)-1]=area_data.proposed_area
                                        theareaunit_list[len(thearea_list)-1]=instance.area_units
                                        therecorddate_list[len(therecorddate_list)-1]=area_data.record_date
                                else: #the change happend after closing date hence the change will have effect the following year
                                    
                                    thearea_list.append(area_data.proposed_area)
                                    theareaunit_list.append(instance.area_units)
                                    therecorddate_list.append(datetime.date(area_data.record_date.year+1,1,1))
                            if not closingdate:
                                if (therecorddate_list[len(thearea_list)-1] <= area_data.record_date and area_data.record_date<=self.billing_date ):
                                    thearea_list[len(thearea_list)-1]=area_data.proposed_area
                                    theareaunit_list[len(thearea_list)-1]=instance.area_units
                                    therecorddate_list[len(therecorddate_list)-1]=area_data.record_date
                        else:#diffrent year changes
                            closingdate =False
                            for closingdata in Bill_finale.objects.all().filter(period = area_data.record_date.year):
                                closingdate = True
                                if area_data.record_date <=closingdata.closing_date:
                                    thearea_list.append(area_data.proposed_area)
                                    theareaunit_list.append(instance.area_units)
                                    therecorddate_list.append(area_data.record_date)
                                else: #the change happend after closing date hence the change will have effect the following year
                                    thearea_list.append(area_data.proposed_area)
                                    theareaunit_list.append(instance.area_units)
                                    therecorddate_list.append(datetime.date(area_data.record_date.year+1,1,1))
                            if not closingdate:
                                thearea_list.append(area_data.proposed_area)
                                theareaunit_list.append(instance.area_units)
                                therecorddate_list.append(area_data.record_date)

                    else:#initial insertio
                        if area_data.description=='Initial':
                            thearea_list.append(area_data.proposed_area)
                            theareaunit_list.append(instance.area_units)
                            therecorddate_list.append(area_data.record_date)
                        else:#description is another thing else
                            closingdate = False
                            for closingdata in Bill_finale.objects.all().filter(period = area_data.record_date.year):
                                closingdate = True
                                if area_data.record_date <=closingdata.closing_date:
                                    thearea_list.append(area_data.proposed_area)
                                    theareaunit_list.append(instance.area_units)
                                    therecorddate_list.append(area_data.record_date)
                                else: #the change happend after closing date hence the change will have effect the following year
                                    thearea_list.append(area_data.proposed_area)
                                    theareaunit_list.append(instance.area_units)
                                    therecorddate_list.append(datetime.date(area_data.record_date.year+1,1,1))  
                            if not closingdate:
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
                            closingdate = False
                            for closingdata in Bill_finale.objects.all().filter(period = landuse_data.record_date.year):
                                closingdate = True
                                if landuse_data.record_date <=closingdata.closing_date:                
                                    if (recorddate_list[len(landusetype_list)-1] <=landuse_data.record_date and landuse_data.record_date<=self.billing_date ):
                                        landusetype_list[len(landusetype_list)-1]=landuse_data.proposed_land_use_id
                                        recorddate_list[len(recorddate_list)-1]=landuse_data.record_date
                                else: #the change happend after closing date hence the change will have effect the following year
                                    
                                    landusetype_list.append(landuse_data.proposed_land_use_id)
                                    recorddate_list.append(datetime.date(landuse_data.record_date.year+1,1,1))
                            if not closingdate:
                                if (recorddate_list[len(landusetype_list)-1] <= landuse_data.record_date and landuse_data.record_date<=self.billing_date ):
                                    landusetype_list[len(landusetype_list)-1]=landuse_data.proposed_land_use_id
                                    recorddate_list[len(recorddate_list)-1]=landuse_data.record_date
                        else:#diffrent year changes
                            closingdate =False
                            for closingdata in Bill_finale.objects.all().filter(period = landuse_data.record_date.year):
                                closingdate = True
                                if landuse_data.record_date <=closingdata.closing_date:
                                    landusetype_list.append(landuse_data.proposed_land_use_id)
                                    recorddate_list.append(landuse_data.record_date)
                                else: #the change happend after closing date hence the change will have effect the following year
                                    landusetype_list.append(landuse_data.proposed_land_use_id)
                                    recorddate_list.append(datetime.date(landuse_data.record_date.year+1,1,1))
                            if not closingdate:
                                landusetype_list.append(landuse_data.proposed_land_use_id)
                                recorddate_list.append(landuse_data.record_date)

                    else:#initial insertio
                        if landuse_data.description=='Initial':
                            landusetype_list.append(landuse_data.proposed_land_use_id)
                            recorddate_list.append(landuse_data.record_date)
                        else:#description is another thing else
                            closingdate = False
                            for closingdata in Bill_finale.objects.all().filter(period = landuse_data.record_date.year):
                                closingdate = True
                                if landuse_data.record_date <=closingdata.closing_date:
                                    landusetype_list.append(landuse_data.proposed_land_use_id)
                                    recorddate_list.append(landuse_data.record_date)
                                else: #the change happend after closing date hence the change will have effect the following year
                                    landusetype_list.append(landuse_data.proposed_land_use_id)
                                    recorddate_list.append(datetime.date(landuse_data.record_date.year+1,1,1))  
                            if not closingdate:
                                landusetype_list.append(landuse_data.proposed_land_use_id)
                                recorddate_list.append(landuse_data.record_date) 



                if len(landusetype_list)==0:
                    landusetype_list.append(instance.landuse_type_id)
                    recorddate_list.append(instance.registration_date)
                i = 0
                
                for dat in landusetype_list:
                    
                    i+=1

                

                #Get start and finish periods...
                start_period = 0
                end_period   = 0

                if instance.lastpayment_period == None:
                    start_period = instance.registration_date.year
                    end_period   = self.billing_date.year
                else:
                    start_period = (instance.lastpayment_period+1)
                    end_period   = self.billing_date.year

                #now we will set a dictionery for { period: landuse}
                 
                dict_landuse = {}
                done         = False
                index        = 0
                count        = 0
                temp_start   = start_period
                temp_end     = end_period
                count        = 0

                while not done:
                    if temp_start<=end_period:
                        if recorddate_list[count].year==temp_start:
                            dict_landuse[temp_start] = landusetype_list[count]
                            temp_start+=1
                            if count<(len(recorddate_list)-1):
                                count+=1
                            
                        elif recorddate_list[count].year>temp_start:
                            dict_landuse[temp_start] = landusetype_list[count-1]
                            temp_start+=1
                        else:
                            dict_landuse[temp_start] = landusetype_list[count]
                            temp_start+=1
                            if count<(len(recorddate_list)-1):
                                count+=1    
                    else:
                        done = True        

                #now we will set a dictionery for { period: area}
                 
                dict_area         = {}
                dict_areaunits    = {}
                done              = False
                index             = 0
                count             = 0
                temp_start        = start_period
                temp_end          = end_period


                while not done:
                    if temp_start<=end_period:
                        if therecorddate_list[count].year==temp_start:
                            dict_area[temp_start] = thearea_list[count]
                            dict_areaunits[temp_start] = theareaunit_list[count]
                            temp_start+=1
                            if count<(len(therecorddate_list)-1):
                                count+=1
                                
                        elif therecorddate_list[count].year>temp_start:
                            dict_area[temp_start] = thearea_list[count-1]
                            dict_areaunits[temp_start] = theareaunit_list[count-1]
                            temp_start+=1
                            
                        else:
                            dict_area[temp_start] = thearea_list[count]
                            dict_areaunits[temp_start] = theareaunit_list[count]
                            temp_start+=1
                            if count<(len(therecorddate_list)-1):
                                count+=1
                    else:
                        done = True        
                cursor.execute("INSERT INTO testing (name,description) VALUES (%s,%s)",["lease number",instance.lease_number])    
                for key,value in dict_area.items():
                    cursor.execute("INSERT INTO testing (name,description) VALUES (%s,%s)",[key,value])    
                #now we are dow with dictionery that has a key as a year and value as land type for that year....

                i = 0
                length = len(dict_landuse)

                total_amt      = 0
                fixedrate_list = []
                landuse_list   = []
                zonenum_list   = []
                area_list      = []
                aunits_list    = []
                period_list    = []
                penalty_list   = []
                amount_list    = []
                if len(dict_landuse)>0:

                    
                    for reference_data in reference_table.objects.all().filter(period__gte=start_period).filter(period__lte=end_period).order_by('period'):
                        
                        if i < len(dict_landuse):
                           
                            if reference_data.period == list(dict_landuse)[i] and reference_data.landuse_type_id==dict_landuse[list(dict_landuse)[i]] and reference_data.zone_number == instance.zone_number:
                                
                                if reference_data.period < self.billing_date.year:
                                    fixedrate_list.append(reference_data.fixed_rate)
                                    landuse_list.append(reference_data.landuse_type_id)
                                    zonenum_list.append(reference_data.zone_number)
                                    area_list.append(dict_area[reference_data.period])
                                    aunits_list.append(instance.area_units)
                                    period_list.append(reference_data.period)
                                    penalty_list.append(reference_data.penalty)
                                    total_amt+=round((reference_data.fixed_rate*(100+reference_data.penalty)/100)*dict_area[reference_data.period],2)
                                    amount_list.append(round((reference_data.fixed_rate*(100+reference_data.penalty)/100)*dict_area[reference_data.period],2))
                                    i+=1   
                
                                else:
                                    fixedrate_list.append(reference_data.fixed_rate)
                                    landuse_list.append(reference_data.landuse_type_id)
                                    zonenum_list.append(reference_data.zone_number)
                                    area_list.append(dict_area[reference_data.period])
                                    aunits_list.append(instance.area_units)
                                    period_list.append(reference_data.period)
                                    penalty_list.append(0)
                                    total_amt+=round(reference_data.fixed_rate*dict_area[reference_data.period],2)
                                    amount_list.append(reference_data.fixed_rate*dict_area[reference_data.period])
                                    i+=1

                cursor = connection.cursor()
                cursor.execute("select nextval('invoicenumber') ")

                order_number = cursor.fetchone()

                today = datetime.date.today()
                year = u'%4s' % today.year
                month = u'%02i' % today.month
                day = u'%02i' % today.day

                new_number = u'%06i' % order_number
                newresult =  "INV-"+year+month+day+new_number                                        

                cursor.execute("INSERT INTO lease_bills_bill (billing_date,invoice_number,balance,lease_number_id,bill_description) VALUES (%s,%s,%s,%s,%s)",[self.billing_date,newresult,total_amt,instance.id,self.bill_description])       
                index = 0
                for data in fixedrate_list:
                    cursor.execute("INSERT INTO lease_bills_bill_details (period , official_area ,area_units, penalty , fixed_rate , amount , invoice_number , landuse_type_id,zone_number) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",[period_list[index],area_list[index],aunits_list[index],penalty_list[index],fixedrate_list[index],amount_list[index],newresult,landuse_list[index],zonenum_list[index]])
                    index+=1
                

                
                
class Bill_details(Model):
    
    invoice_number      = models.CharField(max_length=255)
    period              = models.IntegerField( choices=[(r,r) for r in range(1900, datetime.date.today().year+2)], default=current_year)
    official_area       = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.00)])
    area_units          = models.CharField(max_length=255)
    landuse_type        = models.ForeignKey(Landuse_Type,on_delete=models.CASCADE)
    penalty             = models.DecimalField(max_digits=4, decimal_places=2,validators=[MinValueValidator(0.01),MaxValueValidator(100)])
    fixed_rate          = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.00)])
    amount              = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.00)])
    zone_number         = models.PositiveIntegerField (choices=ZONE,default=1)

class Bill_finale(Model):
    
    closing_date        = models.DateField(auto_now=False,default=date.today)
    period              = models.IntegerField( choices=[(r,r) for r in range(1900, datetime.date.today().year+2)], default=current_year,unique=True)
    description         = models.CharField(max_length=255) 

    class Meta:
        verbose_name = 'Bill Closing'
        verbose_name_plural = 'Bill Closings'
       

    def save(self,*args,**kwargs):
        with connection.cursor() as cursor:
            cursor.execute ("INSERT INTO lease_bills_bill_finale (closing_date,period,description) VALUES (%s,%s,%s)",[self.closing_date,self.closing_date.year,self.description])
            