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
