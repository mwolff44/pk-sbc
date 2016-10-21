from django import template    

from datetime import datetime

register = template.Library()    

@register.filter('timestamp_to_time')
def convert_timestamp_to_time(timestamp):
    """ {{ value|timestamp_to_time|date:"jS N, Y" }} """

    return datetime.fromtimestamp(int(timestamp))