"""
from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import AbstractBaseUser,Permission,User
from datetime import  date
from django.db import connection
import base64
import hashlib
import secrets
from passlib.hash import django_bcrypt_sha256 #django_pbdfk2_sha256

ALGORITHM = "pbkdf2_sha256"

from django.contrib import admin
from django.forms import CheckboxSelectMultiple

class MyModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


class user(AbstractBaseUser):
    record_date         = models.DateField(auto_now=True)
    First_name          = models.CharField(max_length=100,blank=True)
    Last_name           = models.CharField(max_length=100,blank=True)
    user_name           = models.CharField(max_length=100, unique=True)
    email               = models.EmailField(unique=True)
    role                = models.CharField(max_length=100)
    last_login          = models.DateField(blank=True,default=date.today)
    is_staff            = models.BooleanField(default=True)
    is_active           = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)
    password            = models.CharField(max_length=100)
    #confirm_password    = models.CharField(max_length=100)
    USERNAME_FIELD      = 'email'
    
    def __str__(self):
        return self.user_name


    def save(self,*args,**kwargs):
        
        with connection.cursor() as cursor:
            passw = django_bcrypt_sha256.encrypt(self.password)
            if self.pk:
                #get Username for this 
                for dataset in user.objects.all().filter(id=self.pk)[:1]:
                    Username = dataset.user_name
                
                cursor.execute("UPDATE auth_user SET username = %s, first_name =%s, last_name = %s, email =%s, is_staff=%s, is_active=%s WHERE username= %s",[self.user_name,self.First_name,self.Last_name,self.email,self.is_staff,self.is_active,Username])

            else:     
                cursor.execute("INSERT INTO auth_user ( password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[passw,date.today(),'f',self.user_name,self.First_name,self.Last_name,self.email,self.is_staff,self.is_active,date.today()])
        super(user,self).save(*args,*kwargs)


    

class user_permission(models.Model):
    user_name        = models.OneToOneField(user,on_delete=models.CASCADE)
    leases           = models.CharField(max_length =255,blank=True)
    bills            = models.CharField(max_length =255,blank=True)
    Reference_table  = models.CharField(max_length =255,blank=True)
    bill_closing     = models.CharField(max_length =255,blank=True)
    change_landuse   = models.CharField(max_length =255,blank=True)
    modify_area      = models.CharField(max_length =255,blank=True)
    surrender_lease  = models.CharField(max_length =255,blank=True)
    user_profile     = models.CharField(max_length =255,blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.leases:
            self.leases= eval(self.leases)
        if self.bills:
            self.bills= eval(self.bills)
        if self.Reference_table:
            self.Reference_table= eval(self.Reference_table)
        if self.bill_closing:
            self.bill_closing= eval(self.bill_closing)
        if self.change_landuse:
            self.change_landuse= eval(self.change_landuse)
        if self.modify_area:
            self.modify_area= eval(self.modify_area)
        if self.surrender_lease:
            self.surrender_lease= eval(self.surrender_lease)  
        if self.user_profile:
            self.user_profile= eval(self.user_profile)

    def save(self,*args,**kwargs):
        with connection.cursor() as cursor:
            id = 0

    

            count = 0
            for data in User.objects.all().order_by('-id')[:1]:
                id        = data.id

            if self.pk:
                list_leases = str(self.leases).strip("][").replace("'","").split(",")
                cursor.execute("DELETE FROM auth_user_user_permissions WHERE user_id = %s",[id])    
                for ldata in list_leases:
                    if ldata!='':
                        cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])

                list_bills = str(self.bills).strip("][").replace("'","").split(",")  
                for ldata in list_bills:
                    if ldata!='':
                        cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])

                list_rt = str(self.Reference_table).strip("][").replace("'","").split(",")  
                for ldata in list_rt:
                    if ldata!='':
                        cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])

                list_bc = str(self.bill_closing).strip("][").replace("'","").split(",")  
                for ldata in list_bc:
                    if ldata!='':
                        cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])

                list_cl = str(self.change_landuse).strip("][").replace("'","").split(",")  
                for ldata in list_cl:
                    if ldata!='':
                        cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])

                list_ma = str(self.modify_area).strip("][").replace("'","").split(",")  
                for ldata in list_ma:
                    if ldata!='':
                        cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])

                list_sl = str(self.surrender_lease).strip("][").replace("'","").split(",")  
                for ldata in list_sl:
                    if ldata!='':
                        cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])

                list_up = str(self.user_profile).strip("][").replace("'","").split(",")  
                for ldata in list_up:
                    if ldata!='':
                        cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])
            else:
                list_leases = str(self.leases).strip("][").replace("'","").split(",")    
                for ldata in list_leases:
                    if ldata!='':
                        cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])

                list_bills = str(self.bills).strip("][").replace("'","").split(",")  
                for ldata in list_bills:
                    if ldata!='':
                        cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])

                list_rt = str(self.Reference_table).strip("][").replace("'","").split(",")  
                for ldata in list_rt:
                    if ldata!='':
                        cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])

                list_bc = str(self.bill_closing).strip("][").replace("'","").split(",")  
                for ldata in list_bc:
                    if ldata!='':
                        cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])

                list_cl = str(self.change_landuse).strip("][").replace("'","").split(",")  
                for ldata in list_cl:
                    if ldata!='':
                        cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])

                list_ma = str(self.modify_area).strip("][").replace("'","").split(",")  
                for ldata in list_ma:
                    if ldata!='':
                        cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])

                list_sl = str(self.surrender_lease).strip("][").replace("'","").split(",")  
                for ldata in list_sl:
                    if ldata!='':
                        cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])

                list_up = str(self.user_profile).strip("][").replace("'","").split(",")  
                for ldata in list_up:
                    if ldata!='':
                        cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])
                                                        
        super(user_permission,self).save(*args,*kwargs) 
"""

