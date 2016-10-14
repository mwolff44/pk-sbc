from django import template
import datetime, qsstats
from django.db.models import Sum, Avg, Count, Max, Min

from pyfreebill.views import time_series
from pyfreebill.models import Company, DimCustomerDestination, DimCustomerHangupcause, CDR

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