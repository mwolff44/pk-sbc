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

from qsstats import QuerySetStats


def round_value(value):
    """
    Round the given value to 2 decimal place.

    If the value is 0 or None, then simply return 0.
    """
    if value:
        return round(float(value), 2)
    else:
        return 0


# Get variable from request
def getvar(request, field_name, setsession=False):
    """Check field in POST/GET request and return field value
    if there is value you can also save a session variable
    """
    if request.method == 'GET':
        if field_name in request.GET:
            val = request.GET[field_name]
        else:
            val = ''

    if request.method == 'POST':
        if field_name in request.POST:
            val = request.POST[field_name]
        else:
            val = ''

    if setsession and val and val != '':
        request.session['session_' + field_name] = val

    return val


def return_query_string(query_string, postvalue):
    """
    test query_string and if none add &%s
    """
    if query_string:
        query_string += '&%s' % (postvalue)
    else:
        query_string = postvalue

    return query_string


def time_series(queryset, date_field, interval, func=None):
    qsstats = QuerySetStats(queryset, date_field, func)
    return qsstats.time_series(*interval)
