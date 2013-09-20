# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from base_modules import BaseChart, BaseCharts
from django.utils.translation import ugettext_lazy as _
from pyfreebill.models import DimCustomerDestination

class SalesChart(BaseChart):
    """
Dashboard module with sales charts.

With default values it is suited best for 2-column dashboard layouts.
"""
    title = _('Sales stats')
    template = 'admin/pyfreebill/stats/chart.html'
    chart_size = "580x100"
    days = None
    interval = 'days'
    queryset = DimCustomerDestination.objects.all()
    date_field = 'date'


class SalesCharts(BaseCharts):
    """ Group module with 3 default sales charts """
    title = _('Sales')
    chart_model = SalesChart
