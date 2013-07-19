import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Sum, Avg
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from qsstats import QuerySetStats
from pyfreebill.models import DimCustomerDestination

def time_series(queryset, date_field, interval, func=None):
    qsstats = QuerySetStats(queryset, date_field, func)
    return qsstats.time_series(*interval)

@staff_member_required
def admin_report_view(request):
    # view code
    qs = DimCustomerDestination.objects.all()

#    qss_total_calls = qsstats.QuerySetStats(qs, 'date__date', aggregate=Sum('total_calls'))
#    qss_success_calls = qsstats.QuerySetStats(qs, 'date__date', aggregate=Sum('success_calls'))
#    qss_total_duration = qsstats.QuerySetStats(qs, 'date__date', aggregate=Sum('total_duration'))
#    qss_total_sell = qsstats.QuerySetStats(qs, 'date__date', aggregate=Sum('total_sell'))
#    qss_total_cost = qsstats.QuerySetStats(qs, 'date__date', aggregate=Sum('total_cost'))

    today = datetime.date.today()
    firstday = today - datetime.timedelta(days=60)

    ts_total_calls = time_series(qs, 'date__date', [firstday, today], func=Sum('total_calls'))
    ts_success_calls = time_series(qs, 'date__date', [firstday, today], func=Sum('success_calls'))
    ts_total_duration = time_series(qs, 'date__date', [firstday, today], func=Sum('total_duration'))
    ts_total_sell = time_series(qs, 'date__date', [firstday, today], func=Sum('total_sell'))
    ts_total_cost = time_series(qs, 'date__date', [firstday, today], func=Sum('total_cost'))

    return render_to_response('admin/admin_report.html', locals(),
        context_instance=RequestContext(request))
