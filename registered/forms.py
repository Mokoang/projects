from django import forms
from .models import lease, surrendered_lease,adjusted_area,alter_LandUse,Landuse_Type
from django.db.models import Q

# lease Form
class leaseForm( forms.ModelForm ):
  lease_number = forms.CharField(widget=forms.TextInput(attrs={'id':'myField'}), required=True)
  #land_use     = forms.ModelChoiceField(queryset=Landuse_Type.objects.all())
  area_units   = forms.CharField(widget=forms.HiddenInput(), label='')

  class Meta:
      model = lease
      fields = ['lease_number', 'landuse_type','zone_number','registration_date','lastpayment_date','lastpayment_period','area','area_units']
      labels ={"area_units":"",}
      field_order = ['lease_number', 'landuse_type','area','area_units','zone_number','registration_date','lastpayment_date','lastpayment_period']

      def __init__(self, *args, **kwargs):
        self.order_fields(self.Meta.fields)


class surrendered_leaseForm( forms.ModelForm ):
  comments = forms.CharField(widget=forms.Textarea, required=False)
  class Meta:
    model = surrendered_lease
    fields = '__all__'


class alter_landuseForm( forms.ModelForm ):
  comments              = forms.CharField(widget=forms.Textarea, required=False)
  proposed_land_use     = forms.ModelChoiceField(queryset=Landuse_Type.objects.filter(~Q(landuse = alter_LandUse.proposed_land_use)))

  class Meta:
      model = alter_LandUse
      fields = '__all__'        


class Landuse_choicesForm( forms.ModelForm ):
  class Meta:
    model = Landuse_Type
    fields = '__all__'        

   
class adjusted_areasForm( forms.ModelForm ):
  comments = forms.CharField(widget=forms.Textarea, required=False)
  class Meta:
      model = adjusted_area
      fields = '__all__'
