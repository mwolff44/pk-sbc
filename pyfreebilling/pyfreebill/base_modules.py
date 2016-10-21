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
from datetime import timedelta
from django.utils.translation import ugettext_lazy as _
import datetime

from qsstats import QuerySetStats
from admin_tools.dashboard import modules


class BaseChart(modules.DashboardModule):
    """
Dashboard module with user registration charts.

With default values it is suited best for 2-column dashboard layouts.
"""
    title = _('Stats chart')
    template = 'admin/pyfreebill/stats/chart.html'
    chart_size = "580x100"
    days = None
    interval = 'days'
    queryset = None
    date_field = 'date'

    def is_empty(self):
        return False

    def __init__(self, *args, **kwargs):
        super(BaseChart, self).__init__(*args, **kwargs)

        if self.days is None:
            self.days = {'days': 30, 'weeks': 30*7, 'months': 30*12}[self.interval]

        self.data = self.get_data(self.interval, self.days)
        self.prepare_template_data(self.data)

    def get_caption(self, dt):
        return {
            'days': dt.day,
            'months': dt.strftime("%b"),
            'weeks': dt.strftime('%W'),
        }[self.interval]

    # @cached(60*5)
    def get_data(self, interval, days):
        """ Returns an array with new users count per interval """
        stats = QuerySetStats(self.queryset, self.date_field)
        today = datetime.date.today()
        begin = today - datetime.timedelta(days=days-1)
        return stats.time_series(begin, today, interval)

    def prepare_template_data(self, data):
        """ Prepares data for template (it is passed as module attributes) """
        self.captions = [self.get_caption(t[0]) for t in data]
        self.values = [t[1] for t in data]
        self.max_value = max(self.values)



class BaseCharts(modules.Group):
    """ Group module with 3 default registration charts """
    title = _('Stats')
    chart_model = BaseChart

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('children', self.get_charts())
        super(BaseCharts, self).__init__(*args, **kwargs)

    def get_charts(self):
        """ Returns 3 basic chart modules (per-day, per-week and per-month) """
        return [
            self.chart_model(_('By Day'), interval='days'),
            self.chart_model(_('By Week'), interval='weeks'),
            self.chart_model(_('By Month'), interval='months'),
        ]
