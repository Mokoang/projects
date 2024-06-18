from django import forms
from reference_tables.models import reference_table,Landuse_Type,billing_period
from django.db.models import Q
from datetime import  date

class referencetableForm(forms.ModelForm ):
    
    class Meta:
        model = reference_table
        fields = ['landuse_type','zone_number','period','fixed_rate','penalty']


class Landuse_choicesForm( forms.ModelForm ):
  class Meta:
    model = Landuse_Type
    fields = '__all__'        

class bpForm(forms.ModelForm ):
    comments =forms.CharField(widget =forms.Textarea, required=False)
    #billing_period_state = forms.ChoiceField()
    class Meta:
        model = billing_period
        fields = ['period','period_state','comments']

    
    def __init__(self, *args, **kwargs):
        super(bpForm, self).__init__(*args, **kwargs)
        found = False
        for instance in billing_period.objects.all().order_by("-id")[:1]:
            found = True
            if instance.period_state == 'A':
                self.initial['period_state'] = 'I'
                self.initial['period'] = instance.period    
                self.fields['period'].disabled = True
                self.fields['period'].initial = self.instance.period
                self.fields['period_state'].disabled = True
                self.fields['period_state'].initial = self.instance.period_state
            else:        
                self.initial['period_state'] = 'A' 
                self.fields['period_state'].disabled = True
                self.fields['period_state'].initial = self.instance.period_state                
        if not found:
            self.initial['period_state'] = 'A' 
            self.fields['period_state'].disabled = True
            self.fields['period_state'].initial = self.instance.period_state                    
