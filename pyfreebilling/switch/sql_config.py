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

# from migrate_sql.config import SQLItem

from migrate_sql.config import SQLItem

sql_items = [
    SQLItem(
        'dispatcher_view',   # name of the item
        'DROP VIEW IF EXISTS dispatcher CASCADE; '
        'CREATE OR REPLACE VIEW dispatcher AS'
        '  SELECT row_number() OVER () AS id,'
        '  CAST(fsp.direction AS INTEGER) AS setid,'
        '  CAST((CONCAT(\'sip:\', fsp.ip, \':\', sp.sip_port)) AS VARCHAR) AS destination,'
        '  0 AS flags,'
        '  fsp.priority,'
        '  CAST(\'\' AS VARCHAR) AS attrs,'
        '  fsp.description '
        'FROM fs_switch_profile fsp '
        'LEFT JOIN fs_switch f'
        '  ON fsp.fsswitch_id = f.id AND fsp.direction = 1 AND f.setid=10 AND f.enabled=TRUE '
        'LEFT JOIN sip_profile sp'
        '  ON sp.enabled = TRUE AND sp.id = fsp.sipprofile_id; '
        '',  # forward sql
        reverse_sql='DROP VIEW IF EXISTS dispatcher CASCADE; ',  # sql for removal
    ),
    SQLItem(
        'domain_view',   # name of the item
        'DROP VIEW IF EXISTS domain CASCADE; '
        'CREATE OR REPLACE VIEW domain AS'
        '  SELECT row_number() OVER () AS id,'
        '  domain,'
        '  did,'
        '  date_modified AS last_modified '
        'FROM uid_domain ud;'
        '',  # forward sql
        reverse_sql='DROP VIEW IF EXISTS domain CASCADE; ',  # sql for removal
    ),
]
