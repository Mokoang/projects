from django import forms
from .models import reference_table,Bill,verification,correction
from django.db.models import Q


class referencetableForm(forms.ModelForm ):
    
    class Meta:
        model = reference_table
        fields = ['landuse_type','zone_number','period','fixed_rate','penalty']

class lvForm(forms.ModelForm ):
    comments =forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = verification
        fields = ['verification_date','period','comments']

class lcForm(forms.ModelForm ):
    comments =forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = correction
        fields = ['correction_date','correction_status','comments']



class invoiceForm(forms.ModelForm):

  class Meta:
    model   = Bill
    fields = ['billing_date','bill_description','lease_number','balance']
    exclude = ['lease_number','balance']
