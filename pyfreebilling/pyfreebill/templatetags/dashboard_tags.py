# coding: utf-8
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

from django import template
import datetime
from django.db.models import Sum

from ..utils import time_series
from ..models import Company, DimCustomerDestination, DimCustomerHangupcause

register = template.Library()

@register.inclusion_tag('snippets/general_stats.html')
def companies_list():
    company_list = Company.objects.filter(customer_enabled=True)
    return {'companies' : company_list}


@register.inclusion_tag('snippets/dashboard.html')
def total_stats():
    qs_d = DimCustomerDestination.objects.all()
    qs_h = DimCustomerHangupcause.objects.all()


    today = datetime.date.today()
    firstday = today - datetime.timedelta(days=30)

    ts_total_calls = time_series(qs_h, 'date__date', [firstday, today], func=Sum('total_calls'))
    ts_success_calls = time_series(qs_d, 'date__date', [firstday, today], func=Sum('success_calls'))
    ts_total_duration = time_series(qs_d, 'date__date', [firstday, today], func=Sum('total_duration'))
    ts_total_sell = time_series(qs_d, 'date__date', [firstday, today], func=Sum('total_sell'))
    ts_total_cost = time_series(qs_d, 'date__date', [firstday, today], func=Sum('total_cost'))
    return locals()


def get_num_user_orders(parser, token):
    try:
        tag_name, user = token.split_contents()
        return NumUserOrdersNode(user)
    except IndexError:
        raise template.TemplateSyntaxError(
            "%r tag requires a user as it's first argument" % tag_name)


class NumUserOrdersNode(template.Node):
    def __init__(self, user):
        self.user = template.Variable(user)

    def render(self, context):
        return Order.objects.filter(user=self.user.resolve(context)).count()


register.tag('num_orders', get_num_user_orders)