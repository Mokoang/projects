from lease_bills.models import Bill
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.
def report(request):
  return render_to_response('lease_bills/report.html',{'book_list' : Bill.objects.all()},RequestContext(request, {}),)
report = staff_member_required(report)