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

from django.db import models
from django.utils.translation import ugettext_lazy as _


class RoutesDid(models.Model):
    """
    routing plan
    """
    contract_did = models.ForeignKey(
        'did.Did',
        on_delete=models.CASCADE,
    )
    order = models.IntegerField(default=1)
    ROUTE_TYPE_CHOICES = (
        ('s', _(u'SIP Trunk')),
        ('e', _(u'External number')),
    )
    type = models.CharField(_(u'Route type'),
                            max_length=2,
                            choices=ROUTE_TYPE_CHOICES,
                            default='m',
                            help_text=_(u"""Routing type : sip trunk (s) or
                                external number (e)."""))
    trunk = models.ForeignKey(
        'customerdirectory.CustomerDirectory',
        #  limit_choices_to={'company': contract_did__customer__company}
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    number = models.CharField(_(u'destination number'),
                              max_length=30,
                              null=True,
                              blank=True,
                              default='')
    description = models.TextField(_(u'description'),
                                   blank=True)
    date_added = models.DateTimeField(_(u'date added'),
                                      auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'),
                                         auto_now=True)

    class Meta:
        db_table = 'did_routes'
        app_label = 'did'
        ordering = ('contract_did', )
        unique_together = ('contract_did', 'order')
        verbose_name = _(u'DID route')
        verbose_name_plural = _(u'DID routes')

    def __unicode__(self):
        return u"%s pos:%s (type:%s / %s %s)" % (self.contract_did,
                                                 self.order,
                                                 self.type,
                                                 self.number,
                                                 self.trunk)
