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

# VOIP SWITCH

class VoipSwitch(models.Model):
    """ 
    VoipSwitch Profile
    
    Sample config looks like this:
    
    <configuration name="event_socket.conf" description="Socket Client">
      <settings>
        <param name="listen-ip" value="127.0.0.1"/>
        <param name="listen-port" value="8021"/>
        <param name="password" value="ClueCon"/>
      </settings>
    </configuration>
    """

    name = models.CharField(_(u"Switch name"), max_length=50, help_text=_(u"Switch name"))
    ip = models.CharField(_(u"switch IP"), max_length=100, default="auto", help_text=_(u"Switch IP."))
    esl_listen_ip =  models.CharField(_(u"event socket switch IP"), max_length=100, default="127.0.0.1", help_text=_(u"Event socket switch IP."))
    esl_listen_port = models.PositiveIntegerField(_(u"event socket switch port"), default="8021", help_text=_(u"Event socket switch port."))
    esl_password =  models.CharField(_(u"event socket switch password"), max_length=30, default="ClueCon", help_text=_(u"Event socket switch password."))
    date_added = models.DateTimeField(_(u'date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'), auto_now=True)

    class Meta:
        db_table = 'fs_switch'
        app_label = 'switch'
        ordering = ('name', )
        verbose_name = _(u'VoIP Switch')
        verbose_name_plural = _(u'VoIP Switches')

    def __unicode__(self):
        return u"%s (:%s)" % (self.name, self.ip)
