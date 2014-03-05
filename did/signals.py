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
from django.db.models.signals import post_save
from django.contrib import messages
from django.template import Context, loader
from django.utils.translation import ugettext_lazy as _

from switch import esl

from did.models import Did


def update_did(sender, instance, **kwargs):
    """ generate new did xml config file """
    try:
        t = loader.get_template('xml/00_did.xml')
    except IOError:
        messages.error(_(u"""did config xml file update failed.
            Can not load template file !"""))
    dids = Did.objects.all()
    c = Context({"dids": dids, })
    try:
        f = open('/usr/local/freeswitch/conf/dialplan/public/00_did.xml', 'w')
        try:
            f.write(t.render(c))
            f.close()
            try:
                esl.getReloadDialplan()
                messages.success(_(u"FS successfully reload"))
            except IOError:
                messages.error(_(u"""DID config xml file update failed.
                    FS update failed ! Try manually"""))
        finally:
            #f.close()
            messages.success(_(u"DID config xml file update success"))
    except IOError:
        messages.error(_(u"""DID config xml file update failed. Can not
            create file !"""))


post_save.connect(update_did, sender=Did)
