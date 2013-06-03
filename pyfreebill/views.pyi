from django.contrib.admin.views.decorators import stall_member_required
from django.shortcuts import render_to_response
from django_tables2   import RequestConfig
from pyfreebill.models import CDR
from pyfreebill.tables import CDRTable
import qsstats

@staff_member_required
def admin_report_view(request):
    # blabla
    return render_to_response('admin_report.html', 
        context_instance=RequestContext(request))


def report(request):
    objets = CDR.objects.all()
    #RequestConfig(request).configure(table)
    #table1 = "azrty"
    return render_to_response('admin/report.html', {'report' : objets})
