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
        'FROM pyfb_normalization_rule n '
        'LEFT JOIN pyfb_normalization_rule_grp nrp'
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
        'FROM pyfb_call_mapping_rule c) v;'
        '',  # forward sql
        reverse_sql='DROP VIEW IF EXISTS dialplan CASCADE; ',  # sql for removal
    ),
]

# DROP VIEW IF EXISTS dialplan CASCADE; CREATE OR REPLACE VIEW dialplan AS SELECT row_number() OVER () AS id, * FROM (  SELECT  n.name,  nrp.dpid_id AS dpid,  nrp.pr,  n.match_op,  n.match_exp,  n.match_len,  n.subst_exp,  n.repl_exp,  n.attrs,  n.description FROM pyfb_normalization_rule n LEFT JOIN pyfb_normalization_rule_grp nrp  ON n.id = nrp.rule_id UNION ALL SELECT  name,  dpid,  pr,  match_op,  match_exp,  match_len,  subst_exp,  repl_exp,  attrs,  description FROM pyfb_call_mapping_rule c) v;
