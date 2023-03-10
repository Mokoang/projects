from django import forms
from .models import user_permission,user
from django.contrib.auth.models import Permission

for thevalue in Permission.objects.all():
    if thevalue.codename=='view_lease':
        data   = thevalue.id
    elif thevalue.codename=='add_lease':  
        data1  = thevalue.id
    elif thevalue.codename=='change_lease':
       data2 = thevalue.id  
    elif thevalue.codename=='delete_lease':
       data3 = thevalue.id 
       
LEASE_CHOICES = [(data,'View'),(data1,'Add'),(data2,'Edit'),(data3,'Delete')]

for thevalue in Permission.objects.all():
    if thevalue.codename=='view_bill':
        data   = thevalue.id
    elif thevalue.codename=='add_bill':  
        data1  = thevalue.id
    elif thevalue.codename=='change_bill':
       data2 = thevalue.id  
    elif thevalue.codename=='delete_bill':
       data3 = thevalue.id 
       
BILL_CHOICES = [(data,'View'),(data1,'Add'),(data2,'Edit'),(data3,'Delete')]


for thevalue in Permission.objects.all():
    if thevalue.codename=='view_reference_table':
        data   = thevalue.id
    elif thevalue.codename=='add_reference_table':  
        data1  = thevalue.id
    elif thevalue.codename=='change_reference_table':
       data2 = thevalue.id  
    elif thevalue.codename=='delete_reference_table':
       data3 = thevalue.id 

RT_CHOICES = [(data,'View'),(data1,'Add'),(data2,'Edit'),(data3,'Delete')]


for thevalue in Permission.objects.all():
    if thevalue.codename=='view_bill_finale':
        data   = thevalue.id
    elif thevalue.codename=='add_bill_finale':  
        data1  = thevalue.id
    elif thevalue.codename=='change_bill_finale':
       data2 = thevalue.id  
    elif thevalue.codename=='delete_bill_finale':
       data3 = thevalue.id 
BF_CHOICES = [(data,'View'),(data1,'Add'),(data2,'Edit'),(data3,'Delete')]


for thevalue in Permission.objects.all():
    if thevalue.codename=='view_alter_landuse':
        data   = thevalue.id
    elif thevalue.codename=='add_alter_landuse':  
        data1  = thevalue.id
    elif thevalue.codename=='change_alter_landuse':
       data2 = thevalue.id  
    elif thevalue.codename=='delete_alter_landuse':
       data3 = thevalue.id 
CL_CHOICES = [(data,'View'),(data1,'Add'),(data2,'Edit'),(data3,'Delete')]


for thevalue in Permission.objects.all():
    if thevalue.codename=='view_adjusted_area':
        data   = thevalue.id
    elif thevalue.codename=='add_adjusted_area':  
        data1  = thevalue.id
    elif thevalue.codename=='change_adjusted_area':
       data2 = thevalue.id  
    elif thevalue.codename=='delete_adjusted_area':
       data3 = thevalue.id 
CA_CHOICES = [(data,'View'),(data1,'Add'),(data2,'Edit'),(data3,'Delete')]

for thevalue in Permission.objects.all():
    if thevalue.codename=='view_surrendered_lease':
        data   = thevalue.id
    elif thevalue.codename=='add_surrendered_lease':  
        data1  = thevalue.id
    elif thevalue.codename=='change_surrendered_lease':
       data2 = thevalue.id  
    elif thevalue.codename=='delete_surrendered_lease':
       data3 = thevalue.id 
SL_CHOICES = [(data,'View'),(data1,'Add'),(data2,'Edit'),(data3,'Delete')]


for thevalue in Permission.objects.all():
    if thevalue.codename=='view_user':
        data   = thevalue.id
    elif thevalue.codename=='add_user':  
        data1  = thevalue.id
    elif thevalue.codename=='change_user':
       data2 = thevalue.id  
    elif thevalue.codename=='delete_user':
       data3 = thevalue.id 
UP_CHOICES = [(data,'View'),(data1,'Add'),(data2,'Edit'),(data3,'Delete')]

class upForm( forms.ModelForm ):
  leases          = forms.MultipleChoiceField(choices=LEASE_CHOICES, widget=forms.CheckboxSelectMultiple(),required=False)
  bills            = forms.MultipleChoiceField(choices=BILL_CHOICES,  widget=forms.CheckboxSelectMultiple(),required=False)
  Reference_table  = forms.MultipleChoiceField(choices=RT_CHOICES,  widget=forms.CheckboxSelectMultiple(),required=False)
  bill_closing     = forms.MultipleChoiceField(choices=BF_CHOICES,  widget=forms.CheckboxSelectMultiple(),required=False)
  change_landuse   = forms.MultipleChoiceField(choices=CL_CHOICES,  widget=forms.CheckboxSelectMultiple(),required=False)
  modify_area      = forms.MultipleChoiceField(choices=CA_CHOICES,  widget=forms.CheckboxSelectMultiple(),required=False)
  surrender_lease  = forms.MultipleChoiceField(choices=SL_CHOICES,  widget=forms.CheckboxSelectMultiple(),required=False)
  user_profile     = forms.MultipleChoiceField(choices=UP_CHOICES,  widget=forms.CheckboxSelectMultiple(),required=False)
 
  class Meta:
    model = user_permission
    fields = '__all__'

class userForm (forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = user
        
        fields = ('user_name','First_name','Last_name', 'email','password','role','is_staff','is_active')

class changeuserForm (forms.ModelForm):
    #password = forms.CharField(widget=forms.PasswordInput,required=False)
    class Meta:
        model = user
        exclude = ("password","is_superuser",)
