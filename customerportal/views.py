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
from django.views.generic import FormView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.contrib.auth.views import login
from django.shortcuts import get_object_or_404

from braces.views import LoginRequiredMixin

import datetime

from pyfreebill.models import Company, Person, CompanyBalanceHistory, CDR, CustomerDirectory

from customerportal.forms import CDRSearchForm


class HomePageCustView(LoginRequiredMixin, TemplateView):
    template_name = 'customer/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageCustView, self).get_context_data(**kwargs)
        messages.info(self.request, 'Wellcome')
        usercompany = get_object_or_404(Person, user=self.request.user)
        context['company'] = get_object_or_404(Company, name=usercompany.company)
        if context['company'].low_credit_alert > context['company'].customer_balance:
        	messages.warning(self.request, 'ALERT : Low balance (credit alert level : %s)' % context['company'].low_credit_alert)
        if context['company'].account_blocked_alert_sent:
        	messages.danger(self.request, 'ALERT : Account blocked - no remaining credit - Please make an urgent payment')


        # integrer dernier flux financier - page historique
        # integrer panneau contact et stats
        # pages recherche cdr - liste cdr
        # integrer money
        # integrer facture
        # integrer prestation
        return context


class SipAccountCustView(LoginRequiredMixin, ListView):
    template_name = 'customer/sip_account.html'
    context_object_name = 'sipaccount'
    paginate_by = 10
    model = CustomerDirectory

    def get_queryset(self):
        self.usercompany = get_object_or_404(Person, user=self.request.user)
        self.company = get_object_or_404(Company, name=self.usercompany.company)
        return CustomerDirectory.objects.filter(company=self.company.pk).order_by('id')


class CdrReportCustView(LoginRequiredMixin, FormMixin, ListView):
    template_name = 'customer/cdr_view.html'
    context_object_name = 'Cdr'
#    form_class = CDRSearchForm
    paginate_by = 20
    model = CDR

    def get_queryset(self):
        qs = super(CdrReportCustView, self).get_queryset()

        # set start_date and end_date
        end_date = datetime.date.today() - datetime.timedelta(days=0)
        start_date = end_date - datetime.timedelta(days=30)

        #First print

    	# Get the q GET parameter
    	# date from and to and check value
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
            self.usercompany = get_object_or_404(Person, user=self.request.user)
            self.company = get_object_or_404(Company, name=self.usercompany.company)
            qs.filter(customer=self.company.pk).order_by('-start_stamp').exclude(effective_duration="0")
            return qs
        return qs.none()


class BalanceHistoryCustView(LoginRequiredMixin, ListView):
    template_name = 'customer/balance.html'
    #model = CompanyBalanceHistory
    context_object_name = 'CustomerBalance'
    paginate_by = 10

    def get_queryset(self):
        self.usercompany = get_object_or_404(Person, user=self.request.user)
        self.company = get_object_or_404(Company, name=self.usercompany.company)
        return CompanyBalanceHistory.objects.filter(company=self.company.pk).filter(operation_type='customer').order_by('-date_modified')

    def get_context_data(self, **kwargs):
        context = super(BalanceHistoryCustView, self).get_context_data(**kwargs)
        #usercompany = get_object_or_404(Person, user=self.request.user)
        #context['company'] = get_object_or_404(Company, name=usercompany.company)
        context['company'] = self.company
        return context


class ProfileCustView(LoginRequiredMixin, TemplateView):
    template_name = 'customer/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageCustView, self).get_context_data(**kwargs)
        messages.info(self.request, 'Your profile')
        return context