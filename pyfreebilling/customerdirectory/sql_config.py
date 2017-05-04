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
        'subscriber_view',   # name of the item
        'DROP VIEW IF EXISTS subscriber CASCADE; '
        'CREATE OR REPLACE VIEW subscriber AS'
        '  SELECT row_number() OVER () AS id,'
        '  c.name AS username,'
        '  ud.domain,'
        '  c.password '
        'FROM customer_directory c '
        'LEFT JOIN uid_domain ud '
        ' ON c.domain_id = ud.id '
        'WHERE c.enabled=True and c.registration=True;'
        '',  # forward sql
        reverse_sql='DROP subscriber',  # sql for removal
    ),
    SQLItem(
        'address_view',   # name of the item
        'DROP VIEW IF EXISTS address CASCADE; '
        'CREATE OR REPLACE VIEW address AS'
        ' SELECT row_number() OVER () AS id, * FROM ('
        '  SELECT'
        '  1 AS grp,'
        '  CAST(LEFT(CAST(c.sip_ip AS VARCHAR), LENGTH(CAST(c.sip_ip AS VARCHAR)) - 3) AS VARCHAR) AS ip_addr,'
        '  CAST(RIGHT(CAST(c.sip_ip AS VARCHAR), 2) AS INTEGER) AS mask,'
        '  CAST(c.sip_port AS INTEGER) AS port,'
        '  CAST(c.name AS VARCHAR) AS tag '
        'FROM customer_directory c '
        'WHERE c.enabled=True and c.registration=False '
        'UNION ALL '
        'SELECT'
        '  10 AS grp,'
        '  CAST(sg.proxy AS VARCHAR) AS ip_addr,'
        '  32 AS mask,'
        '  5060 AS port,'
        '  sg.name AS tag '
        'FROM sofia_gateway sg '
        'WHERE sg.enabled=True and sg.register=False) v;'
        '',  # forward sql
        reverse_sql='DROP VIEW IF EXISTS address CASCADE ',  # sql for removal
    ),
    SQLItem(
        'usrpref_view',   # name of the item
        'DROP VIEW IF EXISTS usr_preferences CASCADE; '
        'CREATE OR REPLACE VIEW usr_preferences AS'
        ' SELECT row_number() OVER () AS id, * FROM ('
        '  SELECT DISTINCT'
        '  c.name AS uuid,'
        '  c.name AS username,'
        '  CAST(\'\' AS VARCHAR) AS domain,'
        '  CAST(\'grpnormcallee\' AS VARCHAR) AS attribute,'
        '  CAST(1 AS INT) AS type,'
        '  CAST(nrg.dpid_id AS VARCHAR) AS value,'
        '  CAST(now() AS timestamp without time zone) AS last_modified '
        'FROM customer_directory c '
        'INNER JOIN normalization_grp ng '
        '  ON ng.id = c.callee_norm_id '
        'INNER JOIN normalization_rule_grp nrg'
        '  ON nrg.dpid_id = ng.id '
        'WHERE c.enabled=True '
        'UNION ALL '
        '  SELECT DISTINCT'
        '  c.name AS uuid,'
        '  c.name AS username,'
        '  CAST(\'\' AS VARCHAR) AS domain,'
        '  CAST(\'grpnormcaller\' AS VARCHAR) AS attribute,'
        '  CAST(1 AS INT) AS type,'
        '  CAST(nrg.dpid_id AS VARCHAR) AS value,'
        '  CAST(now() AS timestamp without time zone) AS last_modified '
        'FROM customer_directory c '
        'INNER JOIN normalization_grp ng '
        '  ON ng.id = c.callerid_norm_id '
        'INNER JOIN normalization_rule_grp nrg'
        '  ON nrg.dpid_id = ng.id '
        'WHERE c.enabled=True '
        'UNION ALL '
        '  SELECT DISTINCT'
        '  c.name AS uuid,'
        '  c.name AS username,'
        '  CAST(\'\' AS VARCHAR) AS domain,'
        '  CAST(\'grpnormcalleein\' AS VARCHAR) AS attribute,'
        '  CAST(1 AS INT) AS type,'
        '  CAST(nrg.dpid_id AS VARCHAR) AS value,'
        '  CAST(now() AS timestamp without time zone) AS last_modified '
        'FROM customer_directory c '
        'INNER JOIN normalization_grp ng '
        '  ON ng.id = c.callee_norm_in_id '
        'INNER JOIN normalization_rule_grp nrg'
        '  ON nrg.dpid_id = ng.id '
        'WHERE c.enabled=True '
        'UNION ALL '
        '  SELECT DISTINCT'
        '  c.name AS uuid,'
        '  c.name AS username,'
        '  CAST(\'\' AS VARCHAR) AS domain,'
        '  CAST(\'grpnormcallerin\' AS VARCHAR) AS attribute,'
        '  CAST(1 AS INT) AS type,'
        '  CAST(nrg.dpid_id AS VARCHAR) AS value,'
        '  CAST(now() AS timestamp without time zone) AS last_modified '
        'FROM customer_directory c '
        'INNER JOIN normalization_grp ng '
        '  ON ng.id = c.callerid_norm_in_id '
        'INNER JOIN normalization_rule_grp nrg'
        '  ON nrg.dpid_id = ng.id '
        'WHERE c.enabled=True) v; '
        '',  # forward sql
        reverse_sql='DROP VIEW IF EXISTS usr_preferences CASCADE; ',  # sql for removal
    ),
]
