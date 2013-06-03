from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django_tables2   import RequestConfig
from pyfreebill.models import CDR
from pyfreebill.tables import CDRTable
import datetime, qsstats, simplejson

@staff_member_required
def admin_report_view(request):
    # view code
    qs = CDR.objects.all()
    qss = qsstats.QuerySetStats(qs, 'start_stamp')
    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=7)
    qss_by7day = qss.time_series(seven_days_ago, today, 'days')
    days = [i[0].strftime("%A") for i in qss_by7day]
    number_cdr = [i[1] for i in qss_by7day]
    stats_cdr = []
    for date, value in qss_by7day:
        stats_cdr.append((date.strftime("%A"), value))
    table = simplejson.dumps(stats_cdr)
#    RequestConfig(request).configure(table)

    return render_to_response('admin/admin_report.html', {'table': qs},
        context_instance=RequestContext(request))
