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

from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from pyfreebilling.did.models import Did, RoutesDid

class DidResource(resources.ModelResource):

    class Meta:
        model = Did
        exclude = ('date_added', 'date_modified')


class RoutesDidResource(resources.ModelResource):
    contract_did = fields.Field(
        column_name='did',
        attribute='contract_did',
        widget=ForeignKeyWidget(Did, 'number'))

    class Meta:
        model = RoutesDid
        exclude = ('date_added', 'date_modified')
        export_order = (
            'id',
            'contract_did',
            'order',
            'type',
            'trunk',
            'number',
            'description',)
