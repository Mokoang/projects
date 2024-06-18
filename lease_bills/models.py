from django.db import models
from django.db.models import Model
from django.core.validators import  MinLengthValidator,MinValueValidator,MaxValueValidator
from reference_tables.models import billing_period
from django.db.models import Q
from django.db import connection
from registered.models import lease,lease_details
from reference_tables.models import Landuse_Type
import logging
from datetime import  date
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)
# Create your models here.
#Lease details

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

STATE = (
    ('A','Open'),
    ('I','Close'),
)


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

STATES = (
    ('P','Pre-commit'),
    ('C','Commit'),
    ('D','Deleted'),
    )

HISTORY = (
    ('C','Changed'),
    ('U','Unchanged'),
)

BILL_STATUS = (
    ('Complete','Complete'),
    ('Incomplete','Incomplete'),
)
DISTRICT = (
    ('Maseru','Maseru'),
    ('Mafeteng','Mafeteng'),
    ('Leribe','Leribe'),
    ('Berea','Berea'),
    ("Mohale's Hoek","Mohale's Hoek"),
    ('Botha Bothe','Botha Bothe'),
    ('Mokhotlong','Mokhotlong'),
    ('Thaba Tseka','Thaba Tseka'),
    ('Quthing','Quthing'),
    ("Qacha's Neck","Qacha's Neck")
)
class Bill_dataset(lease):
    class Meta:
        proxy = True
        verbose_name = "Bill Dataset"
        verbose_name_plural = "Bill Datasets"



class Bill(Model):
    billing_date             = models.DateField(auto_now=False,default=date.today)
    lease_number             = models.TextField(max_length=50,unique=True,name="lease_number",validators=[MinLengthValidator(7)])
    bill_description         = models.CharField(max_length=255)
    bill_status              = models.CharField(max_length=50,choices=BILL_STATUS,default ="Complete")
    registration_date        = models.DateField(auto_now = False,default=date.today)
    lastpayment_date         = models.DateField(blank=True,null=True)
    lease_holder             = models.CharField(max_length=100,blank=True,null=True)
    phone_number             = models.CharField(max_length=100,blank=True,null=True)
    address                  = models.CharField(max_length=100,blank=True,null=True)
    district                 = models.CharField(max_length=100,blank=True,null=True)
    bill_period              = models.ForeignKey(billing_period,on_delete=models.CASCADE,limit_choices_to=Q(period_state ='A'))
    
    class Meta:
        verbose_name         = 'Ground Rent Bill'
        verbose_name_plural  = 'Ground Rent Bills'   

                
#billing detail             
class Bill_details(Model): 
    bill_id             = models.ForeignKey(Bill,on_delete=models.CASCADE)
    period              = models.IntegerField( choices=[(r,r) for r in range(1900, datetime.date.today().year+2)], default=current_year)
    bill_description    = models.CharField(max_length=255)
    official_area       = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.00)])
    area_units          = models.CharField(max_length=255)
    landuse_type        = models.ForeignKey(Landuse_Type,on_delete=models.CASCADE)
    penalty             = models.DecimalField(max_digits=4, decimal_places=2,validators=[MinValueValidator(0.00),MaxValueValidator(100)])
    calculated_penalty  = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.00)])
    fixed_rate          = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.00)])
    amount_due          = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.00)])
    amount_paid         = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.00)])
    zone_number         = models.PositiveIntegerField (choices=ZONE,default=1)
    status              = models.CharField(max_length=1,choices=STATUS,default ="A")

    class Meta:
        unique_together = ('bill_id','period')


class Bill_payment(Model):
    payment_date       = models.DateField(auto_now=False,default=date.today)
    lease_number       = models.ForeignKey(lease,on_delete=models.CASCADE,limit_choices_to=Q(lease_status='A'))
    payment_period     = models.IntegerField( choices=[(r,r) for r in range(1900, datetime.date.today().year+1)], blank=True,default=0,null=True) 
    amount_paid        = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.00)])
    reciept_number     = models.CharField(max_length=255,null=True,blank=True)
    invoice_number     = models.CharField(max_length=255,null=True,blank=True)
    
    class Meta:
        verbose_name         = 'Ground Rent Payment'
        verbose_name_plural  = 'Ground Rent Payments' 
        
    def clean(self):
        super().clean()

        # Check registration date
        if self.reciept_number is None and self.invoice_number is None:
            raise ValidationError({'Error: Please ensure that you add either invoice number or reciept number before continuing'})

   
    def save(self, *args, **kwargs):
        # Set payment_period based on the year of payment_date
        self.payment_period = self.payment_date.year
        super(Bill_payment, self).save(*args, **kwargs)
        

class Bill_invoice(Bill_details):
    class Meta:
        proxy               = True
        verbose_name        = "Ground Rent Invoice"
        verbose_name_plural = "Ground Rent Invoices "
        