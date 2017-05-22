# -*- coding: utf-8 -*-
# Copyright 2017 Mathias WOLFF
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

from django.contrib import admin

from . models import Fraud


class FraudAdmin(admin.ModelAdmin):
    list_display_links = ('company', 'customerdirectory')
    list_display = ('company',
                    'customerdirectory',
                    'amount_fraud',
                    'high_amount_alert_sent',
                    'minutes_fraud',
                    'minutes_block_alert',
                    'high_minutes_alert_sent',
                    'account_blocked_alert_sent',
                    'date_modified')
    readonly_fields = ('high_amount_alert_sent',
                       'high_minutes_alert_sent',
                       'account_blocked_alert_sent')
    ordering = ('-date_modified',)
    search_fields = ['^company__name',
                     '^customerdirectory']


#----------------------------------------
# register
#----------------------------------------
admin.site.register(Fraud, FraudAdmin)
