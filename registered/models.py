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
from reference_tables.models import Landuse_Type,reference_table


# Create your models here.
#Lease details

UNITS=((f'm\N{SUPERSCRIPT TWO}',f'm\N{SUPERSCRIPT TWO}'),)

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

HISTORY = (
    ('C','Changed'),
    ('U','Unchanged'),
)
DISTRICT = (
    ('Maseru','Maseru'),
    ('Mafeteng','Mafeteng'),
    ('Leribe','Leribe'),
    ('Berea','Berea'),
    ("Mohale's Hoek","Mohale's Hoek"),
    ('Butha-Buthe','Butha-Buthe'),
    ('Mokhotlong','Mokhotlong'),
    ('Thaba Tseka','Thaba-Tseka'),
    ('Quthing','Quthing'),
    ("Qacha's Neck","Qacha's Neck")
)
def get_super(x):
  normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
  super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
  res = x.maketrans(''.join(normal), ''.join(super_s))
  return x.translate(res)
import datetime

def year_choices():
    return [(r,r) for r in range(1900, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year



   
  
class lease(Model):
    lease_number        = models.TextField(max_length=50,unique=True,name="lease_number",validators=[MinLengthValidator(7)])
    zone_number         = models.PositiveIntegerField (choices=ZONE,default=1)
    area                = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.01)])
    area_units          = models.CharField(max_length=50,default='m\N{SUPERSCRIPT TWO}')
    landuse_type        = models.ForeignKey(Landuse_Type,on_delete=models.CASCADE) 
    lease_status        = models.CharField(max_length=1,choices=STATUS,default ="A")
    tag                 = models.CharField(max_length=100,blank=True,null=True)
    lastpayment_period  = models.IntegerField( choices=[(r,r) for r in range(1900, datetime.date.today().year+1)], blank=True,default=0,null=True) 
    registration_date   = models.DateField(auto_now = False,default=date.today)
    lastpayment_date    = models.DateField(blank=True,null=True)
    lease_history       = models.CharField(max_length=1,choices=HISTORY,default ="U")
    lease_holder        = models.CharField(max_length=250,blank=True,null=True)
    phone_number        = models.CharField(max_length=250,blank=True,null=True)
    address             = models.CharField(max_length=250,blank=True,null=True)
    district            = models.CharField(max_length=100,choices=DISTRICT)
    send_for_bill       = models.BooleanField(default=False,blank=True)

    def __str__(self):
        return self.lease_number


    class Meta:
        verbose_name        = 'Lease'
        verbose_name_plural = 'Leases'
    def clean(self):
        super().clean()

        # Check registration date
        if self.registration_date > date.today():
            raise ValidationError({'registration_date': 'Registration date cannot be in the future.'})
        
        # Check lastpayment date
        if self.lastpayment_date and (self.lastpayment_date < self.registration_date or self.lastpayment_date > date.today()):
            raise ValidationError({'lastpayment_date': 'Invalid lastpayment date.'})

           
    def save(self,*args,**kwargs):
        
        with connection.cursor() as cursor:
            
            # check if we have lastpayment_date or not 

            start_period            = self.registration_date.year
            # check if we have lastpayment_date or not 
            if self.lastpayment_date==None:
                self.lastpayment_period = self.registration_date.year
            else:
                self.lastpayment_period = self.lastpayment_date.year


            
            if not self.pk:
                # New record being saved
                super(lease,self).save(*args,*kwargs)
                while start_period<=date.today().year:
                    fixed_rate   = 0.00
                    penalty_rate = 0.00 
                    for data in reference_table.objects.filter(landuse_type_id=self.landuse_type.id).filter(zone_number=self.zone_number).filter(period=start_period):
                        fixed_rate = data.fixed_rate
                        penalty_rate    = data.penalty                    
                    cursor.execute("INSERT INTO registered_lease_details (lease_number_id,period,zone_number,area,area_units,landuse_type_id,fixed_rate,penalty) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",[self.id,start_period,self.zone_number,self.area,self.area_units,self.landuse_type.id,fixed_rate,penalty_rate])
                    start_period+=1
            else:
            # Existing record being updated
            # check if registration date or lastpayment_date are still the same if different delete all the data in lease_details and start again
                same = True
                for data in lease.objects.filter(id=self.pk):
                    registration_date_str = data.registration_date.strftime('%Y-%m-%d %H:%M:%S')

                    if data.registration_date!=self.registration_date:
                        same = False
                     
                if not same:
                    cursor.execute("DELETE FROM registered_lease_details WHERE lease_number_id = %s",[self.pk])
                    while start_period<=date.today().year:
                        fixed_rate   = 0.00
                        penalty_rate = 0.00 
                        for data in reference_table.objects.filter(landuse_type_id=self.landuse_type.id).filter(zone_number=self.zone_number).filter(period=start_period):
                            fixed_rate      = data.fixed_rate
                            penalty_rate    = data.penalty
                        cursor.execute("INSERT INTO registered_lease_details (lease_number_id,period,zone_number,area,area_units,landuse_type_id,fixed_rate,penalty) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",[self.id,start_period,self.zone_number,self.area,self.area_units,self.landuse_type.id,fixed_rate,penalty_rate])
                        start_period +=1
                super(lease,self).save(*args,*kwargs)           
                # else:
                #     while start_period<=date.today().year:
                #         fixed_rate   = 0.00
                #         penalty_rate = 0.00 
                #         for data in reference_table.objects.filter(landuse_type_0id=self.landuse_type.id).filter(zone_number=self.zone_number).filter(period=start_period):
                #             fixed_rate      = data.fixed_rate
                #             penalty_rate    = data.penalty
                #         #cursor.execute("UPDATE registered_lease_details SET zone_number = %s,area=%s,area_units=%s,landuse_type_id=%s,fixed_rate=%s,penalty=%s WHERE lease_number_id = %s",[self.zone_number,self.area,self.area_units,self.landuse_type.id,fixed_rate,penalty_rate,self.id])
                #         start_period+=1


class lease_details(Model):           
    lease_number        = models.ForeignKey(lease,on_delete=models.CASCADE,limit_choices_to=Q(lease_status='A'))
    period              = models.IntegerField( choices=[(r,r) for r in range(1900, datetime.date.today().year+1)], blank=True,default=0,null=True) 
    zone_number         = models.PositiveIntegerField (choices=ZONE,default=1)
    area                = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.01)])
    area_units          = models.CharField(max_length=50,default='m\N{SUPERSCRIPT TWO}')
    landuse_type        = models.ForeignKey(Landuse_Type,on_delete=models.CASCADE)
    fixed_rate          = models.DecimalField(max_digits=10, decimal_places=3,validators=[MinValueValidator(0.001)])
    penalty             = models.DecimalField(max_digits=5, decimal_places=2,validators=[MinValueValidator(0.01),MaxValueValidator(100)], default=20.23)
   
    class Meta:
        unique_together     = ('lease_number','period')
        verbose_name        = 'Lease Details'
        verbose_name_plural = 'Lease Details'


#surrendered lease model
class surrendered_lease(Model):
    lease_number        = models.OneToOneField(lease,on_delete=models.CASCADE,unique=True,primary_key=True,limit_choices_to=Q(lease_status='A'))
    surrender_date      = models.DateField(auto_now = False,default=date.today)
    comments            = models.CharField(max_length=500,default="No comment")

    class Meta:
        verbose_name        = 'Surrender Lease '
        verbose_name_plural = 'Surrender Leases'
    #update lease Status in lease table when we save the record in surrendered lease..
    def save(self,*args,**kwargs):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE registered_lease SET lease_status = 'I' WHERE lease_number = %s",[self.lease_number.lease_number])
        super(surrendered_lease,self).save(*args,*kwargs)


class adjusted_area(Model):
    lease_number        = models.ForeignKey(lease,on_delete=models.CASCADE,limit_choices_to=Q(lease_status='A'))
    proposed_area       = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.01)])
    area_units          = models.CharField(max_length=50,choices =UNITS,default="square_meters")
    description         = models.CharField(max_length=500,default="Changed to")
    record_date         = models.DateField(auto_now = False,default=date.today)
    comments            = models.CharField(max_length=500,default="No comment")


    class Meta:
        verbose_name        = 'Modify Area'
        verbose_name_plural = 'Modify Areas'
    #update lease Status in lease table when we save the record in surrendered lease..
    def save(self,*args,**kwargs):
        found = False
        with connection.cursor() as cursor:
            for instance in lease.objects.all():
                if instance.lease_number == self.lease_number.lease_number:
                    for instance2 in adjusted_area.objects.all():
                        if instance2.lease_number_id == instance.pk:
                            if instance2.description == 'Initial':
                                found = True
                    if not found:       
                        cursor.execute("INSERT INTO registered_adjusted_area (proposed_area,area_units,lease_number_id,record_date,comments,description) VALUES (%s,%s,%s,%s,%s,%s)",[instance.area,instance.area_units,instance.pk,instance.registration_date,'','Initial'])
            super(adjusted_area,self).save(*args,*kwargs)                
            for dataset in  adjusted_area.objects.all().filter(lease_number = self.lease_number).order_by('-record_date')[:1]:
                cursor.execute("UPDATE registered_lease SET area = %s, area_units= %s  WHERE id = %s",[dataset.proposed_area,dataset.area_units,dataset.lease_number_id])
                #cursor.execute("UPDATE lease_bills_billdata SET area = %s, area_units= %s  WHERE lease_number = %s",[dataset.proposed_area,dataset.area_units,dataset.lease_number.lease_number])
        

class alter_LandUse(Model):
    lease_number        = models.ForeignKey(lease,on_delete=models.CASCADE,limit_choices_to=Q(lease_status='A'))
    proposed_land_use   = models.ForeignKey(Landuse_Type,on_delete=models.CASCADE)
    description         = models.CharField(max_length=500,default="Changed to")
    record_date         = models.DateField(auto_now = False,default=date.today)
    comments            = models.CharField(max_length=500,default="No comment")

    class Meta:
        verbose_name        = 'Change Land use'
        verbose_name_plural = 'Change Land use'    

    #update land use in lease table when we save the record in land use..
    def save(self,*args,**kwargs):
        with connection.cursor() as cursor:
            found = False
            for instance in lease.objects.all():
                if instance.lease_number ==self.lease_number.lease_number:
                    for instance2 in alter_LandUse.objects.all():
                        if instance2.lease_number_id==instance.pk:
                            if instance2.description == 'Initial':
                                found = True
                    if not found:       
                        cursor.execute("INSERT INTO registered_alter_landuse (proposed_land_use_id,lease_number_id,record_date,comments,description) VALUES (%s,%s,%s,%s,%s)",[instance.landuse_type.pk,instance.pk,instance.registration_date,'','Initial'])

            super(alter_LandUse,self).save(*args,*kwargs)
            landuseid = 0
            leasenumberid = 0
            for dataset in  alter_LandUse.objects.all().filter(lease_number = self.lease_number).order_by('-record_date')[:1]:
                cursor.execute("UPDATE registered_lease     SET landuse_type_id = %s WHERE id = %s",[dataset.proposed_land_use_id,dataset.lease_number_id])
                #cursor.execute("UPDATE lease_bills_billdata SET landuse_type_id = %s WHERE lease_number = %s",[dataset.proposed_land_use_id,dataset.lease_number.lease_number])
            
class customUserManager(UserManager):
    def _create_user (self,email,password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid email address!")

        email = self.normalize_email(email)
        user  =  self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)

        return user

