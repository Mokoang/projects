from django import forms
from .models import Bill,Bill_dataset
from django.db.models import Q
from datetime import  date



# class billDatasetForm(forms.ModelForm):
#     class Meta:
#         model = Bill_dataset
#         fields = [ 'address']

#     def clean(self):
#         cleaned_data = super().clean()
#         # Remove validation errors for excluded fields
#         all_field_names = [field.name for field in self.Meta.model._meta.get_fields()]
#         excluded_fields = set(all_field_names) - set(self.fields)
#         for field_name in excluded_fields:
#             if field_name in cleaned_data:
#                 del self._errors[field_name]
#         return cleaned_data

    
#     def __init__(self, *args, **kwargs):
#         super(bpForm, self).__init__(*args, **kwargs)
#         found = False
#         for instance in billing_period.objects.all().order_by("-id")[:1]:
#             found = True
#             if instance.period_state == 'A':
#                 self.initial['period_state'] = 'I'
#                 self.initial['period'] = instance.period    
#                 self.fields['period'].disabled = True
#                 self.fields['period'].initial = self.instance.period
#                 self.fields['period_state'].disabled = True
#                 self.fields['period_state'].initial = self.instance.period_state
#             else:        
#                 self.initial['period_state'] = 'A' 
#                 self.fields['period_state'].disabled = True
#                 self.fields['period_state'].initial = self.instance.period_state                
#         if not found:
#             self.initial['period_state'] = 'A' 
#             self.fields['period_state'].disabled = True
#             self.fields['period_state'].initial = self.instance.period_state                    

class invoiceForm(forms.ModelForm):
  #bills_history_validation = forms.BooleanField(label='Compute unchanged lease bills',required=False,widget=forms.widgets.CheckboxInput(attrs={'class':'checkbox-inline'}))
 
 class Meta:
    model   = Bill
    fields  = ['billing_date','bill_description','lease_number','balance','bills_history_validation','bill_period']
    exclude = ['lease_number','balance','bills_history_validation']


 