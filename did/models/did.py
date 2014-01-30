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

#from cities_light.models import City

#from pyfreebill.models import Company


class Did(models.Model):
    """
    DID model
    """
    number = models.CharField(_(u'numeric prefix'),
                              max_length=30,
                              db_index=True)
    city = models.ForeignKey('cities_light.City',
                             blank=True,
                             null=True)
    provider = models.ForeignKey('pyfreebill.Company',
                                 verbose_name=_(u"company"),
                                 limit_choices_to={'supplier_enabled': True})
    plan = models.ForeignKey('did.ProviderRatesDid',
                             verbose_name=_(u"rate plan"),
                             limit_choices_to={'enabled': True})
    max_channels = models.PositiveIntegerField(_(u'max calls'),
                                               default=1,
                                               help_text=_(u"""maximum
                    simultaneous calls allowed for this did."""))
    description = models.TextField(_(u'description'),
                                   blank=True)
    date_added = models.DateTimeField(_(u'date added'),
                                      auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'),
                                         auto_now=True)

    class Meta:
        db_table = 'did'
        app_label = 'did'
        ordering = ('number', )
        verbose_name = _(u'DID')
        verbose_name_plural = _(u'DIDs')

    def __unicode__(self):
        return u"%s (:%s)" % (self.number, self.provider)
