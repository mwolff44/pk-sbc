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

from migrate_sql.config import SQLItem

sql_items = [
    SQLItem(
        'dbaliases_view',   # name of the item
        'DROP VIEW IF EXISTS dbaliases CASCADE; '
        'CREATE OR REPLACE VIEW dbaliases AS'
        '  SELECT row_number() OVER () AS id,'
        '  d.number AS alias_username,'
        '  \'\' AS alias_domain,'
        '  cd.name AS username,'
        '  ud.domain '
        'FROM did_routes dr '
        'LEFT JOIN did d '
        ' ON dr.contract_did_id = d.id AND dr.type = \'s\' '
        'LEFT JOIN customer_directory cd'
        '  ON dr.trunk_id = cd.id '
        'LEFT JOIN uid_domain ud'
        '  ON ud.id = cd.domain_id;'
        '',  # forward sql
        reverse_sql='DROP dbaliases',  # sql for removal
    ),
]
