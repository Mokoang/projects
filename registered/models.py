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
# Create your models here.
#Lease details

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
STATUS = (
    ('A','Active'),
    ('I','Inactive'),
)
import datetime

def year_choices():
    return [(r,r) for r in range(1900, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year

class Landuse_Type(Model):
    landuse        = models.CharField(max_length=255,unique=True)

    class Meta:
        verbose_name = 'Land use Type'
        verbose_name_plural = 'Land use Types'        

    def __str__(self):
        return self.landuse
        
class lease(Model):
    lease_number        = models.TextField(max_length=50,unique=True,name="lease_number",validators=[MinLengthValidator(7)])
    zone_number         = models.PositiveIntegerField (choices=ZONE,default=1)
    area                = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.01)])
    area_units          = models.CharField(max_length=50,default='m\N{SUPERSCRIPT TWO}')
    landuse_type        = models.ForeignKey(Landuse_Type,on_delete=models.CASCADE) 
    lease_status        = models.CharField(max_length=1,choices=STATUS,default ="A")
    lastpayment_period  = models.IntegerField( choices=[(r,r) for r in range(1900, datetime.date.today().year+1)], blank=True,default=0,null=True) 
    registration_date   = models.DateField(auto_now = False,default=date.today)
    lastpayment_date    = models.DateField(blank=True,null=True)
    verified            = models.BooleanField(default=False)
    correction_state    = models.BooleanField(default=True)
    billdata            = models.BooleanField(default=False)

    def __str__(self):
        return self.lease_number


    class Meta:
        verbose_name = 'Lease'
        verbose_name_plural = 'Leases'        

#surrendered lease model
class surrendered_lease(Model):
    lease_number        = models.OneToOneField(lease,on_delete=models.CASCADE,unique=True,primary_key=True)
    surrender_date      = models.DateField(auto_now = False,default=date.today)
    comments            = models.CharField(max_length=500,default="No comment")

    class Meta:
        verbose_name = 'Surrender Lease'
        verbose_name_plural = 'Surrender Leases'
#update lease Status in lease table when we save the record in surrendered lease..
    def save(self,*args,**kwargs):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE registered_lease SET lease_status = 'I' WHERE lease_number = %s",[self.lease_number.lease_number])
        super(surrendered_lease,self).save(*args,*kwargs)


class adjusted_area(Model):
    lease_number        = models.ForeignKey(lease,on_delete=models.CASCADE,limit_choices_to=Q(lease_status='A'))
    proposed_area        = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.01)])
    area_units          = models.CharField(max_length=50,choices =UNITS,default="square_meters")
    description         = models.CharField(max_length=500,default="Changed to")
    record_date         = models.DateField(auto_now = False,default=date.today)
    comments            = models.CharField(max_length=500,default="No comment")


    class Meta:
        verbose_name = 'Modify Area'
        verbose_name_plural = 'Modify Areas'
    #update lease Status in lease table when we save the record in surrendered lease..
    def save(self,*args,**kwargs):
        found = False
        with connection.cursor() as cursor:
            for instance in lease.objects.all():
                if instance.lease_number ==self.lease_number.lease_number:
                    for instance2 in adjusted_area.objects.all():
                        if instance2.lease_number_id==instance.pk:
                            if instance2.description == 'Initial':
                                found = True
                    if not found:       
                        cursor.execute("INSERT INTO registered_adjusted_area (proposed_area,area_units,lease_number_id,record_date,comments,description) VALUES (%s,%s,%s,%s,%s,%s)",[instance.area,instance.area_units,instance.pk,instance.registration_date,'','Initial'])
            super(adjusted_area,self).save(*args,*kwargs)                
            for dataset in  adjusted_area.objects.all().filter(lease_number = self.lease_number).order_by('-record_date')[:1]:
                cursor.execute("UPDATE registered_lease SET area = %s, area_units= %s  WHERE id = %s",[dataset.proposed_area,dataset.area_units,dataset.lease_number_id])
        

class alter_LandUse(Model):
    lease_number        = models.ForeignKey(lease,on_delete=models.CASCADE,limit_choices_to=Q(lease_status='A'))
    proposed_land_use   = models.ForeignKey(Landuse_Type,on_delete=models.CASCADE)
    description         = models.CharField(max_length=500,default="Changed to")
    record_date          = models.DateField(auto_now = False,default=date.today)
    comments            = models.CharField(max_length=500,default="No comment")

    class Meta:
        verbose_name = 'Change Land use'
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
                cursor.execute("UPDATE registered_lease SET landuse_type_id = %s WHERE id = %s",[dataset.proposed_land_use_id,dataset.lease_number_id])
            
class customUserManager(UserManager):
    def _create_user (self,email,password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid email address!")

        email = self.normalize_email(email)
        user  =  self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)

        return user

