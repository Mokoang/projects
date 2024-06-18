
# from django import forms
# from .models import user_permission,user
# from django.contrib.auth.models import Permission


# #Reference Tables (landuse_types,ground rent rates,billing period)
# for thevalue in Permission.objects.all():
#     if thevalue.codename=='view_landuse_type':
#         data   = thevalue.id
#     elif thevalue.codename=='add_landuse_type':  
#         data1  = thevalue.id
#     elif thevalue.codename=='change_landuse_type':
#        data2 = thevalue.id  
#     elif thevalue.codename=='delete_landuse_type':
#        data3 = thevalue.id 
       
# LANDUSE_TYPE_CHOICES = [(data,'View'),(data1,'Add'),(data2,'Edit'),(data3,'Delete')]

# for thevalue in Permission.objects.all():
#     if thevalue.codename=='view_reference_table':
#         data   = thevalue.id
#     elif thevalue.codename=='add_reference_table':  
#         data1  = thevalue.id
#     elif thevalue.codename=='change_reference_table':
#        data2 = thevalue.id  
#     elif thevalue.codename=='delete_reference_table':
#        data3 = thevalue.id 

# GROUNDRENT_RATES_CHOICES = [(data,'View'),(data1,'Add'),(data2,'Edit'),(data3,'Delete')]

# for thevalue in Permission.objects.all():
#     if thevalue.codename=='view_billing_period':
#         data   = thevalue.id
#     elif thevalue.codename=='add_billing_period':  
#         data1  = thevalue.id
#     elif thevalue.codename=='change_billing_period':
#        data2 = thevalue.id  
#     elif thevalue.codename=='delete_billing_period':
#        data3 = thevalue.id 

# BILLING_PERIOD_CHOICES = [(data,'View'),(data1,'Add'),(data2,'Edit'),(data3,'Delete')]

# #Authorization (user)
# for thevalue in Permission.objects.all():
#     if thevalue.codename=='view_user':
#         data   = thevalue.id
#     elif thevalue.codename=='add_user':  
#         data1  = thevalue.id
#     elif thevalue.codename=='change_user':
#        data2 = thevalue.id  
#     elif thevalue.codename=='delete_user':
#        data3 = thevalue.id 
# UP_CHOICES = [(data,'View'),(data1,'Add'),(data2,'Edit'),(data3,'Delete')]

# #Lease Records (Leases,surrender lease,change landuse,modify area)
# for thevalue in Permission.objects.all():
#     if thevalue.codename=='view_lease':
#         data   = thevalue.id
#     elif thevalue.codename=='add_lease':  
#         data1  = thevalue.id
#     elif thevalue.codename=='change_lease':
#        data2 = thevalue.id  
#     elif thevalue.codename=='delete_lease':
#        data3 = thevalue.id 
       
# LEASE_CHOICES = [(data,'View'),(data1,'Add'),(data2,'Edit'),(data3,'Delete')]

# for thevalue in Permission.objects.all():
#     if thevalue.codename=='view_surrendered_lease':
#         data   = thevalue.id
#     elif thevalue.codename=='add_surrendered_lease':  
#         data1  = thevalue.id
#     elif thevalue.codename=='change_surrendered_lease':
#        data2 = thevalue.id  
#     elif thevalue.codename=='delete_surrendered_lease':
#        data3 = thevalue.id 
# SL_CHOICES = [(data,'View'),(data1,'Add'),(data2,'Edit'),(data3,'Delete')]

# for thevalue in Permission.objects.all():
#     if thevalue.codename=='view_alter_landuse':
#         data   = thevalue.id
#     elif thevalue.codename=='add_alter_landuse':  
#         data1  = thevalue.id
#     elif thevalue.codename=='change_alter_landuse':
#        data2 = thevalue.id  
#     elif thevalue.codename=='delete_alter_landuse':
#        data3 = thevalue.id 
# CL_CHOICES = [(data,'View'),(data1,'Add'),(data2,'Edit'),(data3,'Delete')]

# for thevalue in Permission.objects.all():
#     if thevalue.codename=='view_adjusted_area':
#         data   = thevalue.id
#     elif thevalue.codename=='add_adjusted_area':  
#         data1  = thevalue.id
#     elif thevalue.codename=='change_adjusted_area':
#        data2 = thevalue.id  
#     elif thevalue.codename=='delete_adjusted_area':
#        data3 = thevalue.id 
# CA_CHOICES = [(data,'View'),(data1,'Add'),(data2,'Edit'),(data3,'Delete')]

# #Ground rent billing (ground rent payment,ground rent bills,ground rent invoices)
# for thevalue in Permission.objects.all():
#     if thevalue.codename=='view_bill_payment':
#         data   = thevalue.id
#     elif thevalue.codename=='add_bill_payment':  
#         data1  = thevalue.id
#     elif thevalue.codename=='change_bill_payment':
#        data2 = thevalue.id  
#     elif thevalue.codename=='delete_bill_payment':
#        data3 = thevalue.id 
       
# BILL_PAYMENT_CHOICES = [(data,'View'),(data1,'Add'),(data2,'Edit'),(data3,'Delete')]

# for thevalue in Permission.objects.all():
#     if thevalue.codename=='view_bill':
#         data   = thevalue.id
#     elif thevalue.codename=='add_bill':  
#         data1  = thevalue.id
#     elif thevalue.codename=='change_bill':
#        data2 = thevalue.id  
#     elif thevalue.codename=='delete_bill':
#        data3 = thevalue.id 
       
# BILL_CHOICES = [(data,'View'),(data1,'Add'),(data2,'Edit'),(data3,'Delete')]

# for thevalue in Permission.objects.all():
#     if thevalue.codename=='view_bill_invoice':
#         data   = thevalue.id
#     elif thevalue.codename=='add_bill_invoice':  
#         data1  = thevalue.id
#     elif thevalue.codename=='change_bill_invoice':
#        data2 = thevalue.id  
#     elif thevalue.codename=='delete_bill_invoice':
#        data3 = thevalue.id 
       
# BILL_INVOICE_CHOICES = [(data,'View'),(data1,'Add'),(data2,'Edit'),(data3,'Delete')]


# #axes (access attempts,access failures, acess logs)
# for thevalue in Permission.objects.all():
#     if thevalue.codename=='view_accessattempt':
#         data   = thevalue.id
#     elif thevalue.codename=='add_accessattempt':  
#         data1  = thevalue.id
#     elif thevalue.codename=='change_accessattempt':
#        data2 = thevalue.id  
#     elif thevalue.codename=='delete_accessattempt':
#        data3 = thevalue.id 
       
# AXES_ATTEMPT_CHOICES = [(data,'View'),(data1,'Add'),(data2,'Edit'),(data3,'Delete')]

# for thevalue in Permission.objects.all():
#     if thevalue.codename=='view_accessfailurelog':
#         data   = thevalue.id
#     elif thevalue.codename=='add_accessfailurelog':  
#         data1  = thevalue.id
#     elif thevalue.codename=='change_accessfailurelog':
#        data2 = thevalue.id  
#     elif thevalue.codename=='delete_accessfailurelog':
#        data3 = thevalue.id 
       
# AXES_FAILURE_CHOICES = [(data,'View'),(data1,'Add'),(data2,'Edit'),(data3,'Delete')]

# for thevalue in Permission.objects.all():
#     if thevalue.codename=='view_accesslog':
#         data   = thevalue.id
#     elif thevalue.codename=='add_accesslog':  
#         data1  = thevalue.id
#     elif thevalue.codename=='change_accesslog':
#        data2 = thevalue.id  
#     elif thevalue.codename=='delete_accesslog':
#        data3 = thevalue.id 
       
# AXES_LOG_CHOICES = [(data,'View'),(data1,'Add'),(data2,'Edit'),(data3,'Delete')]


# class upForm( forms.ModelForm ):
#     #Reference Tables (landuse_types,ground rent rates,billing period)
#     landuse_type      = forms.MultipleChoiceField(choices=LANDUSE_TYPE_CHOICES, widget=forms.CheckboxSelectMultiple(),required=False)
#     groundrent_rates  = forms.MultipleChoiceField(choices=GROUNDRENT_RATES_CHOICES, widget=forms.CheckboxSelectMultiple(),required=False)
#     billing_periods   = forms.MultipleChoiceField(choices=BILLING_PERIOD_CHOICES, widget=forms.CheckboxSelectMultiple(),required=False)

#     #Authorization (user)
#     user_profile      = forms.MultipleChoiceField(choices=UP_CHOICES, widget=forms.CheckboxSelectMultiple(),required=False)

#     #Lease Records (Leases,surrender lease,change landuse,modify area)
#     leases            = forms.MultipleChoiceField(choices=LEASE_CHOICES, widget=forms.CheckboxSelectMultiple(),required=False)
#     surrender_lease   = forms.MultipleChoiceField(choices=SL_CHOICES, widget=forms.CheckboxSelectMultiple(),required=False)
#     change_landuse    = forms.MultipleChoiceField(choices=CL_CHOICES, widget=forms.CheckboxSelectMultiple(),required=False)
#     modify_area       = forms.MultipleChoiceField(choices=CA_CHOICES, widget=forms.CheckboxSelectMultiple(),required=False)

#     #Ground rent billing (ground rent payment,ground rent bills,ground rent invoices)
#     groundrent_payment= forms.MultipleChoiceField(choices=BILL_PAYMENT_CHOICES, widget=forms.CheckboxSelectMultiple(),required=False)
#     bills             = forms.MultipleChoiceField(choices=BILL_CHOICES, widget=forms.CheckboxSelectMultiple(),required=False)
#     groundrent_invoice= forms.MultipleChoiceField(choices=BILL_INVOICE_CHOICES, widget=forms.CheckboxSelectMultiple(),required=False)

#     #access (access attempts,access failures, acess logs)
#     access_attempts     = forms.MultipleChoiceField(choices=AXES_ATTEMPT_CHOICES, widget=forms.CheckboxSelectMultiple(),required=False)
#     access_failures     = forms.MultipleChoiceField(choices=AXES_FAILURE_CHOICES, widget=forms.CheckboxSelectMultiple(),required=False)
#     access_logs         = forms.MultipleChoiceField(choices=AXES_LOG_CHOICES, widget=forms.CheckboxSelectMultiple(),required=False)    

# class Meta:
#     model = user_permission
#     fields = '__all__'

# class userForm (forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     class Meta:
#         model = user
        
#         fields = ('user_name','First_name','Last_name', 'email','password','role','is_staff','is_active')

# class changeuserForm (forms.ModelForm):
#     #password = forms.CharField(widget=forms.PasswordInput,required=False)
#     class Meta:
#         model = user
#         exclude = ("password","is_superuser",)
