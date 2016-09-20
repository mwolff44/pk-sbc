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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfreebilling. If not, see <http://www.gnu.org/licenses/>
#
# Initial code from Chris Spencer -
# https://github.com/chrisspen/django-admin-steroids

import re

from django.core import urlresolvers
from django.utils.safestring import SafeString, mark_safe
from django.conf import settings

import utils

NONE_STR = '(None)'


class AdminFieldFormatter(object):
    """
    Base class for controlling the display formatting of field values
    in Django's admin.
    how to use :
    from pyfreebilling.formatters import DollarFormat

    class ModelAdmin():
        fields = ('id',
                  'name',
                  DollarFormat('income', decimals=2))
    """

    # Only necessary for logic in admin.helpers.AdminReadonlyField.__init__.
    __name__ = 'AdminFieldFormatter'

    is_readonly = True
    object_level = False
    title_align = None
    null = False

    def __init__(self, name, title=None, **kwargs):
        self.name = name
        self.short_description = kwargs.get('short_description', title or name)
        kwargs.setdefault('allow_tags', True)
        kwargs.setdefault('admin_order_field', name)
        kwargs.setdefault('title_align',
                          kwargs.get('align', kwargs.get('title_align')))
        self.__dict__.update(kwargs)

        if not isinstance(self.short_description, SafeString):
            self.short_description = re.sub(
                '[^0-9a-zA-Z]+',
                ' ',
                self.short_description).capitalize()

            # TODO: Allow markup in short_description? Not practical due to
            # hardcoded escape() in
            # django.contrib.admin.helpers.AdminReadonlyField
#            if self.title_align:
#                title_template = '<span style="text-align:%s">%s</span>'
#                self.short_description = title_template \
#                    % (self.title_align, self.short_description)
#                self.short_description = mark_safe(self.short_description)

    def __call__(self, obj, plaintext=False):
        if self.object_level:
            v = obj
        else:
            if '__' in self.name:
                # Follow Django's double-underscore dereferencing notation.
                parts = self.name.split('__')
                v = obj
                for part in parts:
                    if v is not None:
                        v = getattr(v, part)
            else:
                v = getattr(obj, self.name)
        if callable(v):
            v = v()
        if v is None and self.null:
            return NONE_STR
        if plaintext:
            return self.plaintext(v)
        return self.format(v)

    def format(self, v, plaintext=False):
        return v

    def plaintext(self, *args, **kwargs):
        """
        Called when no HTML is desired.
        """
        kwargs['plaintext'] = True
        return self.format(*args, **kwargs)


class DollarFormat(AdminFieldFormatter):
    """
    Formats a numeric value as dollars.
    """
    decimals = 2
    title_align = 'right'
    align = 'right'
    commas = True

    def format(self, v, plaintext=False):
        if v is None:
            return NONE_STR
        template = '$%.' + str(self.decimals) + 'f'
        if v < 0:
            v *= -1
            template = '('+template+')'
        if self.commas:
            template = utils.FormatWithCommas(template, v)
        else:
            template = template % v
        style = 'display:inline-block; width:100%%; text-align:'+self.align+';'
        if not plaintext:
            template = '<span style="'+style+'">'+template+'</span>'
        return template


class PercentFormat(AdminFieldFormatter):
    """
    Formats a ratio as a percent.
    """
    template = '%.0f%%'
    align = 'right'
    rounder = round

    def format(self, v, plaintext=False):
        if v is None:
            style = 'display:inline-block; width:100%%; text-align:'+self.align+';'
            if not plaintext:
                template = '<span style="'+style+'">'+NONE_STR+'</span>'
            return template
        v *= 100
        v = self.rounder(v)
        template = self.template
        style = 'display:inline-block; width:100%%; text-align:'+self.align+';'
        if not plaintext:
            template = '<span style="'+style+'">'+template+'</span>'
        return template % v


class FloatFormat(AdminFieldFormatter):
    """
    Formats a number as a float.
    """
    decimals = 2
    template = '%.02f'
    align = 'left'
    rounder = round

    def format(self, v, plaintext=False):
        if v is None:
            style = 'display:inline-block; width:100%%; text-align:'+self.align+';'
            if not plaintext:
                template = '<span style="'+style+'">'+NONE_STR+'</span>'
            return template
        v = self.rounder(v, self.decimals)
        template = self.template
        style = 'display:inline-block; width:100%%; text-align:'+self.align+';'
        if not plaintext:
            template = '<span style="'+style+'">'+template+'</span>'
        return template % v


class CenterFormat(AdminFieldFormatter):
    """
    Formats a ratio as a percent.
    """
    title_align = 'center'
    align = 'center'

    def format(self, v, plaintext=False):
        if plaintext:
            return str(v)
        style = 'display:inline-block; width:100%%; text-align:'+self.align+';'
        template = '<span style="'+style+'">%s</span>'
        return template % v


class ReadonlyFormat(AdminFieldFormatter):
    """
    Formats a the field as a readonly attribute.
    """

#    def format(self, v):
#        style = 'display:inline-block; width:100%%; text-align:'+self.align+';'
#        template = '<span style="'+style+'">%s</span>'
#        return template % v


class NbspFormat(AdminFieldFormatter):
    """
    Replaces all spaces with a non-breaking space.
    """

    def format(self, v, plaintext=False):
        v = str(v)
        if plaintext:
            return v
        v = v.replace(' ', '&nbsp;')
        return v


class BooleanFormat(AdminFieldFormatter):
    """
    Converts the field value into a green checkmark image for true and red dash
    image false.
    """
    align = 'left'
    yes_path = '%sadmin/img/icon-yes.gif'
    no_path = '%sadmin/img/icon-no.gif'

    def format(self, v, plaintext=False):
        v = bool(v)
        if plaintext:
            return v
        style = 'display:inline-block; width:100%%; text-align:'+self.align+';'
        template = '<span style="'+style+'"><img src="%s" alt="%s" ' + \
            'title="%s" /></span>'
        if v:
            url = self.yes_path
        else:
            url = self.no_path
        url = url % (settings.STATIC_URL,)
        v = template % (url, v, v)
        return v


class ForeignKeyLink(AdminFieldFormatter):
    """
    Renders a foreign key value as a link to that object's admin change page.
    """
    target = '_blank'
    template_type = 'raw'  # button|raw
    label_template = '{name}'
    null = True

    def format(self, v, plaintext=False):
        try:
            assert self.template_type in ('button', 'raw'), \
                'Invalid template type: %s' % (self.template_type)
            url = utils.get_admin_change_url(v)
            label = self.label_template.format(name=str(v))
            if self.template_type == 'button':
                return ('<a href="%s" target="%s"><input type="button" ' + \
                        'value="%s" /></a>') % (url, self.target, label)
            else:
                return '<a href="%s" target="%s">%s</a>' \
                    % (url, self.target, label)
        except Exception, e:
            return str(e)

    def plaintext(self, v):
        if v is None:
            return ''
        return v.id


class OneToManyLink(AdminFieldFormatter):
    """
    Renders a related objects manager as a link to those object's admin change
    list page.
    """
    object_level = True
    url_param = None
    id_param = 'id'
    target = '_blank'

    def format(self, obj):
        try:
            url = None
            try:
                url = urlresolvers.reverse(self.url_param)
                url = '{0}?{1}={2}'.format(url, self.id_param, obj.id)
            except Exception:
                pass
            q = count = getattr(obj, self.name)
            if hasattr(q, 'count'):
                q = q.all()
                count = q.count()
                if count == 1:
                    # Link directly to the record if only one result.
                    link_obj = q[0]
                    url = utils.get_admin_change_url(link_obj)
                elif count > 1:
                    url = utils.get_admin_changelist_url(q[0])
                    url += '?{1}={2}'.format(url, self.id_param, obj.id)
            if count is None or count == 0:
                return count
            return ('<a href="%s" target="%s"><input type="button" ' + \
                    'value="View %d" /></a>') % (url, self.target, count)
        except Exception, e:
            return str(e)

    def plaintext(self, v):
        return ''  # TODO?
