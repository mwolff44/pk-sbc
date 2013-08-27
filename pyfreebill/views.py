import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Sum, Avg
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from qsstats import QuerySetStats
from pyfreebill.models import DimCustomerDestination

def time_series(queryset, date_field, interval, func=None):
    qsstats = QuerySetStats(queryset, date_field, func)
    return qsstats.time_series(*interval)

@staff_member_required
def admin_status_view(request):
    # print status page
    pfb_version = settings.PFB_VERSION
    return render_to_response('admin/admin_status.html', locals(),
        context_instance=RequestContext(request))

def _margin_series(sell_series, cost_series):
    """
    Substraction between sell time series to cost time series
    """
    sum = 0
    l = []
    for ((d, sell), (_, cost)) in zip(sell_series, cost_series):
        if sell and cost:
            sum += (sell - cost)
        else:
            sum += 0
        l.append((d, sum))
    return l

@staff_member_required
def admin_report_view(request):
    # view code
    qs_d = DimCustomerDestination.objects.all()
    qs_h = DimCustomerHangupcause.objects.all()

#    qss_total_calls = qsstats.QuerySetStats(qs, 'date__date', aggregate=Sum('total_calls'))
#    qss_success_calls = qsstats.QuerySetStats(qs, 'date__date', aggregate=Sum('success_calls'))
#    qss_total_duration = qsstats.QuerySetStats(qs, 'date__date', aggregate=Sum('total_duration'))
#    qss_total_sell = qsstats.QuerySetStats(qs, 'date__date', aggregate=Sum('total_sell'))
#    qss_total_cost = qsstats.QuerySetStats(qs, 'date__date', aggregate=Sum('total_cost'))

    today = datetime.date.today()
    firstday = today - datetime.timedelta(days=7)

    ts_total_calls = time_series(qs_h, 'date__date', [firstday, today], func=Sum('total_calls'))
    ts_success_calls = time_series(qs_d, 'date__date', [firstday, today], func=Sum('success_calls'))
    ts_total_duration = time_series(qs_d, 'date__date', [firstday, today], func=Sum('total_duration'))
    ts_total_sell = time_series(qs_d, 'date__date', [firstday, today], func=Sum('total_sell'))
    ts_total_cost = time_series(qs_d, 'date__date', [firstday, today], func=Sum('total_cost'))
    ts_total_margin = _margin_series(ts_total_sell, ts_total_cost)

    return render_to_response('admin/admin_report.html', locals(),
        context_instance=RequestContext(request))
