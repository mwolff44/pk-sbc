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

#import os
from django.contrib import admin
from pyfreebilling.switch.models import VoipSwitch


class VoipSwitchAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip', 'esl_listen_ip', 'date_modified')
    readonly_fields = ('date_added', 'date_modified')
    list_filter = ('name',)
    ordering = ('name',)

#----------------------------------------
# register
#----------------------------------------
admin.site.register(VoipSwitch, VoipSwitchAdmin)
