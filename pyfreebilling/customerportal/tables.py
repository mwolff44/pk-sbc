# -*- coding: utf-8 -*-
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

# -*- coding: utf-8 -*-

import django_tables2 as tables

from pyfreebilling.pyfreebill.models import CustomerRates


class RatesTable(tables.Table):
    class Meta:
        model = CustomerRates
        per_page = 30
        attrs = {"class": "bootstrap-tables2"}
        fields = (
            "destination",
            "prefix",
            "rate",
            "block_min_duration",
            "minimal_time",
            "init_block")
