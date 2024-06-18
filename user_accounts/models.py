
# from django.db import models
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import AbstractBaseUser,Permission,User
# from datetime import  date
# from django.db import connection
# import base64
# import hashlib
# import secrets
# from passlib.hash import django_bcrypt_sha256 #django_pbdfk2_sha256

# ALGORITHM = "pbkdf2_sha256"

# from django.contrib import admin
# from django.forms import CheckboxSelectMultiple

# class MyModelAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         models.ManyToManyField: {'widget': CheckboxSelectMultiple},
#     }


# class user(AbstractBaseUser):
#     record_date         = models.DateField(auto_now=True)
#     First_name          = models.CharField(max_length=100,blank=True)
#     Last_name           = models.CharField(max_length=100,blank=True)
#     user_name           = models.CharField(max_length=100, unique=True)
#     email               = models.EmailField(unique=True)
#     role                = models.CharField(max_length=100)
#     last_login          = models.DateField(blank=True,default=date.today)
#     is_staff            = models.BooleanField(default=True)
#     is_active           = models.BooleanField(default=False)
#     is_superuser        = models.BooleanField(default=False)
#     password            = models.CharField(max_length=100)
#     #confirm_password    = models.CharField(max_length=100)
#     USERNAME_FIELD      = 'email'
    
#     def __str__(self):
#         return self.user_name


#     def save(self,*args,**kwargs):
        
#         with connection.cursor() as cursor:
#             passw = django_bcrypt_sha256.encrypt(self.password)
#             if self.pk:
#                 #get Username for this 
#                 for dataset in user.objects.all().filter(id=self.pk)[:1]:
#                     Username = dataset.user_name
                
#                 cursor.execute("UPDATE auth_user SET username = %s, first_name =%s, last_name = %s, email =%s, is_staff=%s, is_active=%s WHERE username= %s",[self.user_name,self.First_name,self.Last_name,self.email,self.is_staff,self.is_active,Username])

#             else:     
#                 cursor.execute("INSERT INTO auth_user ( password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[passw,date.today(),'f',self.user_name,self.First_name,self.Last_name,self.email,self.is_staff,self.is_active,date.today()])
#         super(user,self).save(*args,*kwargs)


    

# class user_permission(models.Model):

#     user_name        = models.OneToOneField(user,on_delete=models.CASCADE)
    
#     #Reference Tables (landuse_types,ground rent rates,billing period)
#     landuse_type      = models.CharField(max_length =255,blank=True)
#     groundrent_rates  = models.CharField(max_length =255,blank=True)
#     billing_periods   = models.CharField(max_length =255,blank=True)
    
#     #Authorization (user)
#     user_profile      = models.CharField(max_length =255,blank=True)
    
#     #Lease Records (Leases,surrender lease,change landuse,modify area)
#     leases            = models.CharField(max_length =255,blank=True)
#     surrender_lease   = models.CharField(max_length =255,blank=True)
#     change_landuse    = models.CharField(max_length =255,blank=True)
#     modify_area       = models.CharField(max_length =255,blank=True)
    
#     #Ground rent billing (ground rent payment,ground rent bills,ground rent invoices)
#     groundrent_payment= models.CharField(max_length =255,blank=True)
#     bills             = models.CharField(max_length =255,blank=True)
#     groundrent_invoice= models.CharField(max_length =255,blank=True)
    
#     #access (access attempts,access failures, acess logs)
#     access_attempts     = models.CharField(max_length =255,blank=True)
#     access_failures     = models.CharField(max_length =255,blank=True)
#     access_logs         = models.CharField(max_length =255,blank=True)    
    

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         #Reference Tables (landuse_types,ground rent rates,billing period)
#         if self.landuse_type:
#             self.landuse_type = eval(self.landuse_type)
#         if self.groundrent_rates:
#             self.groundrent_rates = eval(self.groundrent_rates)  
#         if self.billing_periods:
#             self.billing_periods = eval(self.billing_periods)

#         #Authorization (user)            
#         if self.user_profile:
#             self.user_profile= eval(self.user_profile)
            
#         #Lease Records (Leases,surrender lease,change landuse,modify area)            
#         if self.leases:
#             self.leases= eval(self.leases)
#         if self.surrender_lease:
#             self.surrender_lease= eval(self.surrender_lease)  
#         if self.change_landuse:
#             self.change_landuse= eval(self.change_landuse)            
#         if self.modify_area:
#             self.modify_area= eval(self.modify_area)  
            
#         #Ground rent billing (ground rent payment,ground rent bills,ground rent invoices)   
#         if self.groundrent_payment:
#             self.groundrent_payment= eval(self.groundrent_payment)
#         if self.bills:
#             self.bills= eval(self.bills)    
#         if self.groundrent_invoice:
#             self.groundrent_invoice= eval(self.groundrent_invoice)
            
#         #access (access attempts,access failures, acess logs)       
#         if self.access_attempts:
#             self.access_attempts= eval(self.access_attempts)
#         if self.access_failures:
#             self.access_failures= eval(self.access_failures)    
#         if self.access_logs:
#             self.access_logs= eval(self.access_logs)

        


#     def save(self,*args,**kwargs):
#         with connection.cursor() as cursor:
#             id = 0

#             count = 0
#             for data in User.objects.all().order_by('-id')[:1]:
#                 id        = data.id
#             cursor.execute("DELETE FROM auth_user_user_permissions WHERE user_id = %s",[id])   
            
#             #Reference Tables (landuse_types,ground rent rates,billing period)
#             list_landuse_type = str(self.landuse_type).strip("][").replace("'","").split(",")
#             for ldata in list_landuse_type:
#                 if ldata!='':
#                     cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])
#             list_groundrent_rates = str(self.groundrent_rates).strip("][").replace("'","").split(",")
#             for ldata in list_groundrent_rates:
#                 if ldata!='':
#                     cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])
#             list_billing_periods = str(self.billing_periods).strip("][").replace("'","").split(",")
#             for ldata in list_billing_periods:
#                 if ldata!='':
#                     cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])                    
            
#             #Authorization (user)  
#             list_up = str(self.user_profile).strip("][").replace("'","").split(",")  
#             for ldata in list_up:
#                 if ldata!='':
#                     cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])

            
#             #Lease Records (Leases,surrender lease,change landuse,modify area)             
#             list_leases = str(self.leases).strip("][").replace("'","").split(",")
#             for ldata in list_leases:
#                 if ldata!='':
#                     cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])
#             list_sl = str(self.surrender_lease).strip("][").replace("'","").split(",")  
#             for ldata in list_sl:
#                 if ldata!='':
#                     cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])  
#             list_cl = str(self.change_landuse).strip("][").replace("'","").split(",")  
#             for ldata in list_cl:
#                 if ldata!='':
#                     cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])                            
#             list_ma = str(self.modify_area).strip("][").replace("'","").split(",")  
#             for ldata in list_ma:
#                 if ldata!='':
#                     cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata]) 

#             #Ground rent billing (ground rent payment,ground rent bills,ground rent invoices) 
#             list_groundrent_payment = str(self.groundrent_payment).strip("][").replace("'","").split(",")  
#             for ldata in list_groundrent_payment:
#                 if ldata!='':
#                     cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])                
#             list_bills = str(self.bills).strip("][").replace("'","").split(",")  
#             for ldata in list_bills:
#                 if ldata!='':
#                     cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata]) 
#             list_groundrent_invoice = str(self.groundrent_invoice).strip("][").replace("'","").split(",")  
#             for ldata in list_groundrent_invoice:
#                 if ldata!='':
#                     cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])                        

            

#             #access (access attempts,access failures, acess logs)
#             list_access_attempts = str(self.access_attempts).strip("][").replace("'","").split(",")            
#             for ldata in list_access_attempts:
#                 if ldata!='':
#                     cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])
#             list_access_failures = str(self.access_failures).strip("][").replace("'","").split(",")            
#             for ldata in list_access_failures:
#                 if ldata!='':
#                     cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])
#             list_access_logs = str(self.access_logs).strip("][").replace("'","").split(",")            
#             for ldata in list_access_logs:
#                 if ldata!='':
#                     cursor.execute("INSERT INTO auth_user_user_permissions (user_id, permission_id) VALUES (%s,%s)",[id,ldata])
            
#         super(user_permission,self).save(*args,*kwargs) 


