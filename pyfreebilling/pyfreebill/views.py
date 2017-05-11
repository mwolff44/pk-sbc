# Copyright 2013 Mathias WOLFF
# This file is part of pyfreebilling.
#
# pyfreebilling is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfreebilling is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfreebilling.  If not, see <http://www.gnu.org/licenses/>

from django.shortcuts import render_to_response
from django.template import RequestContext, Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Avg, Count, Max, Min
from django.views.generic import TemplateView
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import ugettext_lazy as _

from django_tables2 import RequestConfig

from .utils import time_series
import time
import datetime
import qsstats
import json
import pytz

from pyfreebilling.switch import esl

from pyfreebilling import __version__

from pyfreebilling.cdr.models import CDR

from pyfreebilling.customerdirectory.models import CustomerDirectory

from .utils import round_value, getvar, return_query_string
from .forms import CDRSearchForm
from .models import DimCustomerDestination, DimProviderDestination, DimCustomerHangupcause, Company, SipProfile
from .tables import TopCustTable, TopProvTable, TopDestCustTable, TopDestProvTable


@staff_member_required
def global_stats_view(request, vue):
    # set start_date and end_date
    # default yesterday stats
    if vue == 'customer' or vue == 'dest_customer':
        qs = DimCustomerDestination.objects.all()
    if vue == 'provider' or vue == 'dest_provider':
        qs = DimProviderDestination.objects.all()

    current_tz = pytz.utc
    dt = datetime.datetime.now()
    end_date = datetime.date(dt.year, dt.month, dt.day)
    # end_date = datetime.date(2014, 8, 28)
    start_date = end_date - datetime.timedelta(days=1)
    qs_orderby = '-total_sell'

    # Get the q GET parameter
    # date from and to and check value
    start_d = {'y': [], 'm': [], 'd': [], 'status': True}
    end_d = {'y': [], 'm': [], 'min': [], 'status': True}
    li = ['y', 'm', 'd']
    for i in li:
        start_d[str(i)] = request.GET.get("from_" + str(i))
        if start_d[str(i)] and start_d[str(i)].isnumeric():
            start_d[str(i)] = int(start_d[str(i)])
        else:
            start_d['status'] = False
        end_d[str(i)] = request.GET.get("to_" + str(i))
        if end_d[str(i)] and end_d[str(i)].isnumeric():
            end_d[str(i)] = int(end_d[str(i)])
        else:
            end_d['status'] = False
    # dest num
    dest_num = request.GET.get("dest_num")
    company = request.GET.get("company")
    if start_d['status']:
        start_date = datetime.datetime(
            start_d['y'], start_d['m'], start_d['d'], 00, 00)
    if end_d['status']:
        end_date = datetime.datetime(
            end_d['y'], end_d['m'], end_d['d'], 00, 00)
    if start_date and end_date:
        qs = qs.filter(date__date__range=(start_date, end_date))

    if dest_num:
        qs = qs.filter(destination__startswith=dest_num)

    if company:
        if vue == 'customer' or vue == 'dest_customer':
            qs = qs.filter(customer__name__contains=company)
        if vue == 'provider' or vue == 'dest_provider':
            qs = qs.filter(provider__name__contains=company)

    if vue == 'customer':
        qs1 = qs.values('customer__name', 'customer__cb_currency__code')
    if vue == 'dest_customer' or vue == 'dest_provider':
        qs1 = qs.values('destination')
    if vue == 'provider':
        qs1 = qs.values('provider__name', 'provider__cb_currency__code')
    stats_table = qs1.\
        annotate(total_sell=Sum('total_sell')).\
        annotate(success_calls=Sum('success_calls')).\
        annotate(total_calls=Sum('total_calls')).\
        annotate(total_cost=Sum('total_cost')).\
        annotate(total_duration=Sum('total_duration')).\
        annotate(max_duration=Max('max_duration')).\
        annotate(min_duration=Min('min_duration')).\
        annotate(avg_duration=Min('avg_duration')).\
        order_by('-total_sell')
    total_table = qs.\
        aggregate(total_sell=Sum('total_sell'),
            success_calls=Sum('success_calls'),\
            total_calls=Sum('total_calls'),\
            total_cost=Sum('total_cost'),\
            total_duration=Sum('total_duration'),\
            max_duration=Max('max_duration'),\
            min_duration=Min('min_duration'),\
            avg_duration=Min('avg_duration'))

    if vue == 'customer':
        table = TopCustTable(stats_table)
    if vue == 'dest_customer':
        table = TopDestCustTable(stats_table)
    if vue == 'provider':
        table = TopProvTable(stats_table)
    if vue == 'dest_provider':
        table = TopDestProvTable(stats_table)
    RequestConfig(request, paginate={"per_page": 100}).configure(table)
    #import pdb; pdb.set_trace()
    return render_to_response('admin/customers_stats.html', locals(),
                              context_instance=RequestContext(request))


@staff_member_required
def customers_stats_view(request):
    return global_stats_view(request, vue='customer')


@staff_member_required
def destination_customers_stats_view(request):
    return global_stats_view(request, vue='dest_customer')


@staff_member_required
def providers_stats_view(request):
    return global_stats_view(request, vue='provider')


@staff_member_required
def destination_providers_stats_view(request):
    return global_stats_view(request, vue='dest_provider')


# @staff_member_required
# def FsDirectoryUpdateView(request):
#     messages.info(request, """Reloading FS""")
#     try:
#         t = loader.get_template('xml/directory.conf.xml')
#     except IOError:
#         messages.error(request, """customer sip config xml file update failed.
#             Can not load template file !""")
#     customerdirectorys = CustomerDirectory.objects.filter(
#         company__customer_enabled__exact=True, enabled=True)
#     accounts = Company.objects.filter(customer_enabled=True)
#     c = Context({"customerdirectorys": customerdirectorys,
#                  "accounts": accounts})
#     try:
#         f = open('/usr/local/freeswitch/conf/directory/default.xml', 'w')
#         try:
#             f.write(t.render(c))
#             f.close()
#             try:
#                 fs = esl.getReloadACL()
#                 messages.success(request, "FS successfully reload")
#             except IOError:
#                 messages.error(request, """customer sip config xml file update
#                     failed. FS ACL update failed ! Try manually - %s""" % fs)
#         finally:
#             # f.close()
#             messages.success(request, """customer sip config xml file update
#                 success""")
#     except IOError:
#         messages.error(request, """customer sip config xml file update failed.
#             Can not create file !""")
#     pfb_version = __version__
#     return render_to_response('admin/admin_status.html', locals(),
#                               context_instance=RequestContext(request))


# def FsSofiaUpdateView(request):
#     """ generate new sofia xml config file """
#     try:
#         t = loader.get_template('xml/sofia.conf.xml')
#     except IOError:
#         messages.error(request,
#                        """sofia config xml file update failed. Can not load
#                        template file !""")
#     sipprofiles = SipProfile.objects.all()
#     accounts = Company.objects.filter(supplier_enabled=True)
#     c = Context({"sipprofiles": sipprofiles, "accounts": accounts})
#     try:
#         f = open('/usr/local/freeswitch/conf/autoload_configs/sofia.conf.xml',
#                  'w')
#         try:
#             f.write(t.render(c))
#             f.close()
#             try:
#                 fs = esl.getReloadGateway(request)
#                 messages.success(request, "FS successfully reload")
#             except IOError:
#                 messages.error(request, """customer sip config xml file update
#                     failed. FS ACL update failed ! Try manually -- %s""" % fs)
#         finally:
#             # f.close()
#             messages.success(request, "sofia config xml file update success")
#     except IOError:
#         messages.error(request, """sofia config xml file update failed. Can
#             not create file !""")
#     pfb_version = __version__
#     return render_to_response('admin/admin_status.html', locals(),
#                               context_instance=RequestContext(request))


@staff_member_required
def admin_status_view(request):
    # print status page
    # pfb_version = settings.PFB_VERSION
    pfb_version = __version__
    return render_to_response('admin/admin_status.html', locals(),
                              context_instance=RequestContext(request))


@staff_member_required
def admin_listmodels_view(request):
    # print status page
    # pfb_version = settings.PFB_VERSION

    return render_to_response('admin/list_models.html', locals(),
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


@user_passes_test(lambda u: u.is_superuser)
@staff_member_required
def live_report_view(request):
    """ selecting cdr and live stats calculated from selection """

    form = CDRSearchForm(request.user, request.POST or None)

    if request.method == 'POST':

        if form.is_valid():
            query_string = ''
            query_answer = ''

            tzname = settings.TIME_ZONE
            offset = datetime.datetime.now(
                pytz.timezone(tzname)).strftime('%z')

            from_date = getvar(request, 'from_date_0')
            if from_date:
                formated_date = from_date[0:4] + '-' + from_date[8:10] + '-' + from_date[
                    5:7] + '+' + from_date[11:13] + '%3A' + from_date[14:16] + '%3A00'
                if offset[0] == '+':
                    formated_date = formated_date + '%2B'
                else:
                    formated_date = formated_date + '%2D'
                formated_date = formated_date + \
                    offset[1:3] + '%3A' + offset[3:5]
                date_string = 'start_stamp__gte=' + str(formated_date)
                query_string = return_query_string(query_string, date_string)
                #import pdb; pdb.set_trace()

            to_date = getvar(request, 'to_date_0')
            if to_date:
                formated_date = to_date[0:4] + '-' + to_date[8:10] + '-' + to_date[
                    5:7] + '+' + to_date[11:13] + '%3A' + to_date[14:16] + '%3A00'
                if offset[0] == '+':
                    formated_date = formated_date + '%2B'
                else:
                    formated_date = formated_date + '%2D'
                formated_date = formated_date + \
                    offset[1:3] + '%3A' + offset[3:5]
                date_string = 'start_stamp__lt=' + str(formated_date)
                query_string = return_query_string(query_string, date_string)

            customer_id = getvar(request, 'customer_id')
            if customer_id and customer_id != '0':
                customer_string = 'customer__id__exact=' + str(customer_id)
                query_string = return_query_string(
                    query_string, customer_string)

            provider_id = getvar(request, 'provider_id')
            if provider_id and provider_id != '0':
                provider_string = 'lcr_carrier_id__id__exact=' + \
                    str(provider_id)
                query_string = return_query_string(
                    query_string, provider_string)

            ratecard_id = getvar(request, 'ratecard_id')
            if ratecard_id and ratecard_id != '0':
                ratecard_string = 'ratecard_id__id__exact=' + str(ratecard_id)
                query_string = return_query_string(
                    query_string, ratecard_string)

            lcr_id = getvar(request, 'lcr_id')
            if lcr_id and lcr_id != '0':
                lcr_string = 'lcr_group_id__id__exact=' + str(lcr_id)
                query_string = return_query_string(query_string, lcr_string)

            dest_num = getvar(request, 'dest_num')
            if dest_num:
                dstnum_string = 'destination_number__startswith=' + \
                    str(dest_num)
                query_string = return_query_string(query_string, dstnum_string)

            if query_string:
                query_answer = '/extranet/pyfreebill/cdr/?' + str(query_string)
            else:
                query_answer = '/extranet/pyfreebill/cdr/'

            return HttpResponseRedirect(query_answer)
    else:
        form = CDRSearchForm(request.user)

    request.session['msg'] = ''
    request.session['error_msg'] = ''

    return render_to_response('admin/live_report.html', locals(),
                              context_instance=RequestContext(request))


class ChartData(object):

    @classmethod
    def get_stats_revenue(cls):
        data = []
        data1 = {'key': [], 'values': [], 'color': '#2ca02c'}
        data2 = {'key': [], 'values': []}
        data3 = {'key': [], 'area': 'true', 'values': [], 'color': '#ff7f0e'}
        data4 = {'key': [], 'area': 'true', 'values': [], 'color': '#7777ff'}

        values_sell = []
        values_cost = []
        values_duration = []
        margin = []
        values_margin = []

        qs = CDR.objects.filter(effective_duration__gt="0")
        qs_d = DimCustomerDestination.objects.all()
        # qs_h = DimCustomerHangupcause.objects.all()
        qss_sell = qsstats.QuerySetStats(qs, 'start_stamp',
                                         aggregate=Sum('total_sell'))
        qss_cost = qsstats.QuerySetStats(qs, 'start_stamp',
                                         aggregate=Sum('total_cost'))
        qss_sum_duration = qsstats.QuerySetStats(qs, 'start_stamp',
                                                 aggregate=Sum('effective_duration'))
        today = datetime.date.today() - datetime.timedelta(days=0)
        firstday = today - datetime.timedelta(days=90)
        # stats_sell = qss_sell.time_series(seven_days_ago, today)
        # stats_cost = qss_sell.time_series(seven_days_ago, today)
        # stats_duration = qss_sum_duration.time_series(seven_days_ago, today)

        ts_total_calls = time_series(
            qs_d, 'date__date', [firstday, today], func=Sum('total_calls'))
        ts_success_calls = time_series(
            qs_d, 'date__date', [firstday, today], func=Sum('success_calls'))
        stats_duration = time_series(
            qs_d, 'date__date', [firstday, today], func=Sum('total_duration'))
        stats_sell = time_series(
            qs_d, 'date__date', [firstday, today], func=Sum('total_sell'))
        stats_cost = time_series(
            qs_d, 'date__date', [firstday, today], func=Sum('total_cost'))

        for i in range(len(stats_sell)):
            values_sell.append(
                [int(time.mktime(stats_sell[i][0].timetuple()) * 1000),
                    round_value(stats_sell[i][1])])

        data1['key'].append("Revenue")
        data1['values'] = values_sell
        data.append(data1)

        for i in range(len(stats_sell)):
            temp_data = [
                int(time.mktime(stats_sell[i][0].timetuple()) * 1000),
                # round_value(stats_sell[i][1])
                # round_value(stats_cost[i][1]),
                int(round_value(stats_duration[i][1]))
            ]
            values_duration.append(temp_data)

        data2['values'] = values_duration
        # data2['bar'].append('true')
        data2['key'].append("Duration")
        # data.append(data2)

        for i in range(len(stats_sell)):
            values_cost.append(
                [int(time.mktime(stats_cost[i][0].timetuple()) * 1000),
                    round_value(stats_cost[i][1])])

        data3['key'].append("Cost")
        data3['values'] = values_cost
        data.append(data3)

        for i in range(len(stats_sell)):
            if stats_sell[i][1]:
                if stats_cost[i][1]:
                    margin.append(stats_sell[i][1] - stats_cost[i][1])
                else:
                    margin.append(stats_sell[i][1])
            else:
                if stats_cost[i][1]:
                    margin.append(0 - stats_cost[i][1])
                else:
                    margin.append(0)
            values_margin.append(
                [int(time.mktime(stats_cost[i][0].timetuple()) * 1000),
                    round_value(margin[i])])

        data4['key'].append("Margin")
        data4['values'] = values_margin
        data.append(data4)

        #data = [{"values": [[1400281200000, 3.36], [1400367600000, 0.03], [1400454000000, 30.15], [1400540400000, 34.57], [1400626800000, 30.73], [1400713200000, 32.12], [1400799600000, 60.69], [1400886000000, 3.61], [1400972400000, 0.05], [1401058800000, 68.54], [1401145200000, 339.0], [1401231600000, 130.58], [1401318000000, 17.12], [1401404400000, 133.52], [1401490800000, 111.67], [1401577200000, 0.02], [1401663600000, 640.63], [1401750000000, 565.65], [1401836400000, 646.74], [1401922800000, 639.96], [1402009200000, 798.42], [1402095600000, 493.09], [1402182000000, 65.13], [1402268400000, 380.07], [1402354800000, 17.01], [1402441200000, 388.32], [1402527600000, 0], [1402614000000, 0], [1402700400000, 0], [1402786800000, 0], [1402873200000, 0]], "bar": ["true"], "key": ["Revenue"]}, {"values": [[1400281200000, 25562], [1400367600000, 65], [1400454000000, 232339], [1400540400000, 225068], [1400626800000, 225401], [1400713200000, 198695], [1400799600000, 257652], [1400886000000, 14543], [1400972400000, 92], [1401058800000, 295177], [1401145200000, 980922], [1401231600000, 467542], [1401318000000, 70453], [1401404400000, 369460], [1401490800000, 307402], [1401577200000, 84], [1401663600000, 1814630], [1401750000000, 1578658], [1401836400000, 1799965], [1401922800000, 2344407], [1402009200000, 2540328], [1402095600000, 1345970], [1402182000000, 21832], [1402268400000, 1010094], [1402354800000, 66511], [1402441200000, 1078292], [1402527600000, 0], [1402614000000, 0], [1402700400000, 0], [1402786800000, 0], [1402873200000, 0]], "key": ["Duration"]}]

        return data

    @classmethod
    def get_stats_volume(cls):
        data = []
        data1 = {'key': [], 'values': []}  # , 'color': '#2ca02c'
        data2 = {'key': [], 'values': [], 'bar': 'true'}

        values_duration = []
        values_total_calls = []
        values_success_calls = []

        qs_d = DimCustomerDestination.objects.all()
        #qs_h = DimCustomerHangupcause.objects.all()

        today = datetime.date.today() - datetime.timedelta(days=0)
        firstday = today - datetime.timedelta(days=90)

        ts_total_calls = time_series(
            qs_d, 'date__date', [firstday, today], func=Sum('total_calls'))
        ts_success_calls = time_series(
            qs_d, 'date__date', [firstday, today], func=Sum('success_calls'))
        stats_duration = time_series(
            qs_d, 'date__date', [firstday, today], func=Sum('total_duration'))

        for i in range(len(stats_duration)):
            temp_data = [
                int(time.mktime(stats_duration[i][0].timetuple()) * 1000),
                int(round_value(ts_total_calls[i][1]))]

            values_total_calls.append(temp_data)

        data1['key'].append("Total calls")
        data1['values'] = values_total_calls
        data.append(data1)

        for i in range(len(stats_duration)):
            temp_data = [
                int(time.mktime(stats_duration[i][0].timetuple()) * 1000),
                int(round_value(ts_success_calls[i][1]))]

            values_success_calls.append(temp_data)

        data2['values'] = values_success_calls
        # data2['bar'].append('true')
        data2['key'].append("Success calls")
        data.append(data2)

        return data

    @classmethod
    def get_stats_minute(cls):
        data = []
        data1 = {'key': [], 'values': []}
        data2 = {'key': [], 'bar': 'true', 'values': []}

        values_duration = []
        values_acd = []
        acd = []

        qs_d = DimCustomerDestination.objects.all()
        # qs_h = DimCustomerHangupcause.objects.all()

        today = datetime.date.today() - datetime.timedelta(days=0)
        firstday = today - datetime.timedelta(days=90)

        ts_success_calls = time_series(
            qs_d, 'date__date', [firstday, today], func=Sum('success_calls'))
        stats_duration = time_series(
            qs_d, 'date__date', [firstday, today], func=Sum('total_duration'))

        for i in range(len(stats_duration)):
            if stats_duration[i][1]:
                acd.append(stats_duration[i][1] / ts_success_calls[i][1])
            else:
                acd.append(0)
            temp_data = [
                int(time.mktime(stats_duration[i][0].timetuple()) * 1000),
                acd[i]]

            values_acd.append(temp_data)

        data1['key'].append("ACD in seconds")
        data1['values'] = values_acd
        data.append(data1)

        for i in range(len(stats_duration)):
            temp_data = [
                int(time.mktime(stats_duration[i][0].timetuple()) * 1000),
                int(round_value(stats_duration[i][1]) / 60)]

            values_duration.append(temp_data)

        data2['values'] = values_duration
        # data2['bar'].append('true')
        data2['key'].append("Volume in minutes")
        data.append(data2)

        return data


@staff_member_required
def chart_stats_general_json(request):
    # if not request.method == "POST":
    #     raise PermissionDenied
    data = []
    params = request.GET
    name = params.get('name', '')
    if name == 'revenue':
        data = ChartData.get_stats_revenue()
    elif name == 'volume':
        data = ChartData.get_stats_volume()
    elif name == 'minute':
        data = ChartData.get_stats_minute()

    return HttpResponse(json.dumps(data), content_type='application/json')


@user_passes_test(lambda u: u.is_superuser)
@staff_member_required
def general_stats(request):
    company_list = Company.objects.all()
    # filter(customer_enabled=True)
    datas['companies'] = company_list
    return render_to_response('snippets/general_stats.html',
                              context_instance=RequestContext(request, datas))


@staff_member_required
def companies_list():
    company_list = Company.objects.all()
    # filter(customer_enabled=True)
    return {'companies': company_list}


@user_passes_test(lambda u: u.is_superuser)
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

    ts_total_calls = time_series(
        qs_h, 'date__date', [firstday, today], func=Sum('total_calls'))
    ts_success_calls = time_series(
        qs_d, 'date__date', [firstday, today], func=Sum('success_calls'))
    ts_total_duration = time_series(
        qs_d, 'date__date', [firstday, today], func=Sum('total_duration'))
    ts_total_sell = time_series(
        qs_d, 'date__date', [firstday, today], func=Sum('total_sell'))
    ts_total_cost = time_series(
        qs_d, 'date__date', [firstday, today], func=Sum('total_cost'))
    ts_total_margin = _margin_series(ts_total_sell, ts_total_cost)

    return render_to_response('admin/admin_report.html', locals(),
                              context_instance=RequestContext(request))
