# -*- coding: utf-8 -*-
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

# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView, ListView, View, CreateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from braces.views import LoginRequiredMixin

from django_tables2 import RequestConfig

from djqscsv import render_to_csv_response

import datetime
import calendar

from dateutil.relativedelta import relativedelta

from pyfreebilling.customerdirectory.models import CustomerDirectory

from pyfreebilling.pyfreebill.models import Company,\
    CompanyBalanceHistory,\
    CustomerRates,\
    CustomerRateCards,\
    Person

from pyfreebilling.cdr.models import CDR

from .forms import CDRSearchForm, RatesForm, RatesListFormHelper
from .filters import RatesListFilter
from .tables import RatesTable
from .utils import PagedFilteredTableView


class CreateUserView(CreateView):
    template_name = "customer/register.html"
    model = Person


@login_required
def rates_csv_view(request, *args, **kwargs):
    ratecard = kwargs['ratecard']

    qs = CustomerRates.objects.values(
        'destination',
        'prefix',
        'rate',
        'block_min_duration',
        'minimal_time',
        'init_block')

    try:
        usercompany = Person.objects.get(user=request.user)
        company = get_object_or_404(Company, name=usercompany.company)
        rc = CustomerRateCards.objects.filter(
            company=company.pk)\
            .filter(ratecard__enabled=True)\
            .order_by('priority')
        qs = qs.filter(ratecard__pk=ratecard)
    except Person.DoesNotExist:
        messages.error(request,
                       _(u"""This user is not linked to a customer !"""))

    if ratecard and int(ratecard) and ratecard in rc:
        ratecard = int(ratecard)
        qs = qs.filter(ratecard__pk=ratecard)
    else:
        qs.none()
    return render_to_csv_response(qs,
                                  append_datestamp=True)


@login_required
def csv_view(request, *args, **kwargs):
    day = kwargs['day']
    month = kwargs['month']
    daymonth = None

    qs = CDR.objects.values('customer__name',
                            'caller_id_number',
                            'destination_number',
                            'start_stamp',
                            'billsec',
                            'prefix',
                            'sell_destination',
                            'rate',
                            'init_block',
                            'block_min_duration',
                            'total_sell',
                            'customer_ip',
                            'sip_user_agent'
                            )

    try:
        usercompany = Person.objects.get(user=request.user)
        company = get_object_or_404(Company, name=usercompany.company)
        qs = qs.filter(customer=company.pk)\
               .exclude(effective_duration="0")\
               .order_by('-start_stamp')
    except Person.DoesNotExist:
        messages.error(request,
                       _(u"""This user is not linked to a customer !"""))

    if day and int(day) < 8 and int(day) > 0:
        day = int(day)
        start_date = datetime.date.today() - datetime.timedelta(days=int(day))
        end_date = start_date + datetime.timedelta(days=1)
        daymonth = 'OK'

    if month and int(month) < 4 and int(month) > 0:
        month = int(month)
        dm = datetime.date.today()
        start_date = datetime.date(dm.year, dm.month, 1) - relativedelta(months=int(month))
        end_date = start_date + relativedelta(months=1)
        end_date = end_date - datetime.timedelta(days=1)
        daymonth = 'OK'

    if daymonth:
        qs = qs.filter(start_stamp__range=(start_date, end_date))
    else:
        qs.none()
    # import pdb; pdb.set_trace()
    return render_to_csv_response(
        qs,
        append_datestamp=True,
        field_header_map={'customer__name': 'Customer'})


class Template404View(LoginRequiredMixin, TemplateView):
    template_name = 'customer/404.html'


class Template500View(LoginRequiredMixin, TemplateView):
    template_name = 'customer/500.html'


class ListExportCustView(LoginRequiredMixin, TemplateView):
    template_name = 'customer/report.html'

    def get_context_data(self, **kwargs):
        context = super(ListExportCustView, self).get_context_data(**kwargs)
        context['day_1'] = datetime.date.today() - datetime.timedelta(days=1)
        context['day_2'] = datetime.date.today() - datetime.timedelta(days=2)
        context['day_3'] = datetime.date.today() - datetime.timedelta(days=3)
        context['day_4'] = datetime.date.today() - datetime.timedelta(days=4)
        context['day_5'] = datetime.date.today() - datetime.timedelta(days=5)
        context['day_6'] = datetime.date.today() - datetime.timedelta(days=6)
        context['day_7'] = datetime.date.today() - datetime.timedelta(days=7)
        dm = datetime.date.today()
        context['month_1'] = datetime.date(dm.year, dm.month, 1) - relativedelta(months=1)
        context['month_2'] = datetime.date(dm.year, dm.month, 1) - relativedelta(months=2)
        context['month_3'] = datetime.date(dm.year, dm.month, 1) - relativedelta(months=3)
        return context


class HomePageCustView(LoginRequiredMixin, TemplateView):
    template_name = 'customer/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageCustView, self).get_context_data(**kwargs)
        messages.info(self.request, _(u'Welcome'))
        try:
            usercompany = Person.objects.get(user=self.request.user)
            try:
                context['company'] = Company.objects.get(name=usercompany.company)
                if context['company'].low_credit_alert > context['company'].customer_balance:
                    messages.warning(self.request,
                                     _(u'ALERT : Low balance (credit alert level : %s)') % context['company'].low_credit_alert)
                if context['company'].account_blocked_alert_sent:
                    messages.error(self.request,
                                   _(u'ALERT : Account blocked - no remaining credit - Please make an urgent payment'))
                context['ratecards'] = CustomerRateCards.objects.filter(
                    company=context['company'].pk)\
                    .filter(ratecard__enabled=True)\
                    .order_by('priority')
            except Company.DoesNotExist:
                pass
        except Person.DoesNotExist:
            messages.error(self.request,
                           _(u"""This user is not linked to a customer !"""))

        # integrer panneau contact et stats
        # integrer facture
        # integrer prestation
        return context


class RatesFilteredTableView(PagedFilteredTableView):
    template_name = 'customer/rates_table.html'
    model = CustomerRates
    # queryset = CustomerRates.objects.all()
    table_class = RatesTable
    filter_class = RatesListFilter
    formhelper_class = RatesListFormHelper

    def get_queryset(self, **kwargs):
        qs = super(RatesFilteredTableView, self).get_queryset()
        try:
            self.usercompany = Person.objects.get(user=self.request.user)
            self.company = get_object_or_404(Company,
                                             name=self.usercompany.company)
            self.rc = CustomerRateCards.objects.filter(
                company=self.company.pk)\
                .filter(ratecard__enabled=True)\
                .order_by('priority')
            qs = qs.filter(enabled=True).order_by('destination')
        except Person.DoesNotExist:
            messages.error(self.request,
                           _(u"""This user is not linked to a customer !"""))
        # ratecard
        if self.kwargs['ratecard'] and self.rc.filter(ratecard_id=self.kwargs['ratecard']):
            self.ratecard = self.kwargs['ratecard']
        else:
            self.rc = CustomerRateCards.objects.filter(
                company=self.company.pk)\
                .filter(ratecard__enabled=True)\
                .order_by('priority')
            self.ratecard = self.rc[0].ratecard_id

        if self.ratecard:  # and ratecard.isnumeric():
            qs = qs.filter(ratecard__pk=self.ratecard)
            return qs

        return qs.none()


class StatsCustView(LoginRequiredMixin, TemplateView):
    template_name = 'customer/stats.html'


class SipAccountCustView(LoginRequiredMixin, ListView):
    template_name = 'customer/sip_account.html'
    context_object_name = 'sipaccount'
    paginate_by = 10
    model = CustomerDirectory

    def get_queryset(self):
        qs = super(SipAccountCustView, self).get_queryset()
        try:
            self.usercompany = Person.objects.get(user=self.request.user)
            self.company = get_object_or_404(Company,
                                             name=self.usercompany.company)
            return CustomerDirectory.objects.filter(company=self.company.pk)\
                                            .order_by('id')
        except Person.DoesNotExist:
            messages.error(self.request,
                           _(u"""This user is not linked to a customer !"""))
        return qs.none()


class CdrReportCustView(LoginRequiredMixin, FormMixin, ListView):
    template_name = 'customer/cdr_view.html'
    context_object_name = 'Cdr'
    form_class = CDRSearchForm
    paginate_by = 30
    model = CDR

    def get_queryset(self):
        qs = super(CdrReportCustView, self).get_queryset()
        try:
            self.usercompany = Person.objects.get(user=self.request.user)
            self.company = get_object_or_404(Company,
                                             name=self.usercompany.company)
            qs = qs.filter(customer=self.company.pk)\
                   .exclude(effective_duration="0")\
                   .order_by('-start_stamp')
        except Person.DoesNotExist:
            messages.error(self.request,
                           _(u"""This user is not linked to a customer !"""))

        # set start_date and end_date
        end_date = datetime.date.today() + datetime.timedelta(days=1)
        start_date = end_date - datetime.timedelta(days=30)

        start_d = {'y': [], 'm': [], 'd': [], 'h': [], 'min': [], 'status': True}
        end_d = {'y': [], 'm': [], 'd': [], 'h': [], 'min': [],'status': True}
        li = ['y', 'm', 'd', 'h', 'min']
        for i in li:
            start_d[str(i)] = self.request.GET.get("from_" + str(i))
            if start_d[str(i)] and start_d[str(i)].isnumeric():
                start_d[str(i)] = int(start_d[str(i)])
            else:
                start_d['status'] = False
            end_d[str(i)] = self.request.GET.get("to_" + str(i))
            if end_d[str(i)] and end_d[str(i)].isnumeric():
                end_d[str(i)] = int(end_d[str(i)])
            else:
                end_d['status'] = False
        # dest num
        dest_num = self.request.GET.get("dest_num")
        if start_d['status']:
            start_date = datetime.datetime(start_d['y'], start_d['m'], start_d['d'], start_d['h'], start_d['min'])
        if end_d['status']:
            end_date = datetime.datetime(end_d['y'], end_d['m'], end_d['d'], end_d['h'], end_d['min'])
        if start_date and end_date:
            qs = qs.filter(start_stamp__range=(start_date, end_date))

        if dest_num and dest_num.isnumeric():
            qs = qs.filter(destination_number__startswith=dest_num)

        # test if get succes or not
        if start_d['status'] or end_d['status'] or dest_num:
            return qs
        return qs.none()


class BalanceHistoryCustView(LoginRequiredMixin, ListView):
    template_name = 'customer/balance.html'
    model = CompanyBalanceHistory
    context_object_name = 'CustomerBalance'
    paginate_by = 10

    def get_queryset(self):
        qs = super(BalanceHistoryCustView, self).get_queryset()
        try:
            self.usercompany = Person.objects.get(user=self.request.user)
            self.company = get_object_or_404(Company, name=self.usercompany.company)
            return CompanyBalanceHistory.objects.filter(company=self.company.pk)\
                                                .filter(operation_type='customer')\
                                                .order_by('-date_modified')
        except Person.DoesNotExist:
            messages.error(self.request, _(u"""This user is not linked to a customer !"""))
        return qs.none()

    def get_context_data(self, **kwargs):
        context = super(BalanceHistoryCustView, self).get_context_data(**kwargs)
        try:
            self.usercompany = Person.objects.get(user=self.request.user)
            context['company'] = get_object_or_404(Company, name=self.usercompany.company)
            return context
        except Person.DoesNotExist:
            messages.error(self.request, _(u"""This user is not linked to a customer !"""))
        return context


class ProfileCustView(LoginRequiredMixin, TemplateView):
    template_name = 'customer/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageCustView, self).get_context_data(**kwargs)
        messages.info(self.request, 'Your profile')
        return context
