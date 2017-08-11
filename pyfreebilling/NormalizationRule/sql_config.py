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
        'dialplan_view',   # name of the item
        'DROP VIEW IF EXISTS dialplan CASCADE; '
        'CREATE OR REPLACE VIEW dialplan AS'
        ' SELECT row_number() OVER () AS id, * FROM ('
        '  SELECT'
        '  n.name,'
        '  nrp.dpid_id AS dpid,'
        '  nrp.pr,'
        '  n.match_op,'
        '  n.match_exp,'
        '  n.match_len,'
        '  n.subst_exp,'
        '  n.repl_exp,'
        '  n.attrs,'
        '  n.description '
        'FROM normalization_rule n '
        'LEFT JOIN normalization_rule_grp nrp'
        '  ON n.id = nrp.rule_id '
        'UNION ALL '
        'SELECT'
        '  name,'
        '  dpid,'
        '  pr,'
        '  match_op,'
        '  match_exp,'
        '  match_len,'
        '  subst_exp,'
        '  repl_exp,'
        '  attrs,'
        '  description '
        'FROM call_mapping_rule c) v;'
        '',  # forward sql
        reverse_sql='DROP VIEW IF EXISTS dialplan CASCADE; ',  # sql for removal
    ),
]
