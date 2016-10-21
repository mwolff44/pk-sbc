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

from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

import django_tables2 as tables
from django_tables2.utils import Accessor as A

from decimal import Decimal


class TopTableMixin(tables.Table):
    #customer__name = tables.Column(verbose_name=u'Customer')
    total_sell = tables.Column(
        verbose_name=u'Sell', attrs={"td": {"class": "text-align: right"}})
    total_cost = tables.Column(verbose_name=u'Margin')
    #customer__cb_currency__code = tables.Column(verbose_name=u'Currency')
    success_calls = tables.Column(verbose_name=u'Nb Succes Calls')
    total_calls = tables.Column(verbose_name=u'Nb Calls')
    total_duration = tables.Column()
    avg_duration = tables.Column(verbose_name=u'ACD')
    max_duration = tables.Column(orderable=False)
    min_duration = tables.Column(verbose_name=u'ASR')

    def __init__(self, *args, **kwargs):
        super(TopTableMixin, self).__init__(*args, **kwargs)

    def render_total_cost(self, value, record):
        if record['total_sell'] and record['total_cost']:
            return '%.2f' % \
                float(record['total_sell'] - record['total_cost'])
        else:
            return '0'

    def render_avg_duration(self, value, record):
        if record['success_calls'] and record['total_duration']:
            value = int(record['total_duration'] / record['success_calls'])
            return '%02d:%02d:%02d' % \
                reduce(lambda ll, b: divmod(ll[0], b) + ll[1:],
                       [(value,), 60, 60])
        else:
            return 'N/A'

    def render_total_duration(self, value):
        """ return the value in hh:mm:ss """
        return '%02d:%02d:%02d' % \
            reduce(lambda ll, b: divmod(ll[0], b) + ll[1:],
                   [(value,), 60, 60])

    def render_max_duration(self, value):
        """ return the value in hh:mm:ss """
        return '%02d:%02d:%02d' % \
            reduce(lambda ll, b: divmod(ll[0], b) + ll[1:],
                   [(value,), 60, 60])

    def render_min_duration(self, value, record):
        """ return the ASR Value """
        if record['success_calls'] and record['total_calls']:
            value = Decimal(record['success_calls']) / Decimal(
                record['total_calls'])
            return '{:.0%}'.format(value)
        else:
            return 'N/A'


class TopCustTable(TopTableMixin, tables.Table):

    """ Customers stats table """
    customer__name = tables.Column(verbose_name=u'Customer')
    customer__cb_currency__code = tables.Column(verbose_name=u'Currency')

    def render_customer__name(self, value):
        """ add a link to destination detail """
        return mark_safe("<a href='/extranet/destination_customers_stats/?company=%s'>%s</a>" % (value, value))

    class Meta:
        # bootstrap 2 template from : https://gist.github.com/dyve/5458209
        attrs = {"class": "bootstrap-tables2"}
        sequence = (
            "customer__name", "total_sell", "total_cost", "customer__cb_currency__code",
            "total_calls", "success_calls", "min_duration", "total_duration", "avg_duration", "max_duration")


class TopDestCustTable(TopTableMixin, tables.Table):

    """ Destinations stats table """
    destination = tables.Column(verbose_name=u'Destination')

    def render_destination(self, value):
        """ add a link to destination detail """
        return mark_safe("<a href='/extranet/customers_stats/?destination=%s'>%s</a>" % (value, value))

    class Meta:
        # bootstrap 2 template from : https://gist.github.com/dyve/5458209
        attrs = {"class": "bootstrap-tables2"}
        sequence = (
            "destination", "total_sell", "total_cost",
            "total_calls", "success_calls", "min_duration", "total_duration", "avg_duration", "max_duration")


class TopDestProvTable(TopTableMixin, tables.Table):

    """ Destinations stats table """
    destination = tables.Column(verbose_name=u'Destination')

    def render_destination(self, value):
        """ add a link to destination detail """
        return mark_safe("<a href='/extranet/providers_stats/?destination=%s'>%s</a>" % (value, value))

    class Meta:
        # bootstrap 2 template from : https://gist.github.com/dyve/5458209
        attrs = {"class": "bootstrap-tables2"}
        sequence = (
            "destination", "total_sell", "total_cost",
            "total_calls", "success_calls", "min_duration", "total_duration", "avg_duration", "max_duration")


class TopProvTable(TopTableMixin, tables.Table):

    """ Providers stats table """
    provider__name = tables.Column(verbose_name=u'Provider')
    provider__cb_currency__code = tables.Column(verbose_name=u'Currency')

    def render_provider__name(self, value):
        """ add a link to destination detail """
        return mark_safe("<a href='/extranet/destination_providers_stats/?company=%s'>%s</a>" % (value, value))

    class Meta:
        # bootstrap 2 template from : https://gist.github.com/dyve/5458209
        attrs = {"class": "bootstrap-tables2"}
        sequence = (
            "provider__name", "total_sell", "total_cost", "provider__cb_currency__code",
            "total_calls", "success_calls", "min_duration", "total_duration", "avg_duration", "max_duration")
