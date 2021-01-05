from migrate_sql.config import SQLItem

sql_items = [
    SQLItem(
        'dialplan_view',   # name of the item
        'DROP VIEW IF EXISTS pyfb_direction CASCADE; '
        'CREATE OR REPLACE VIEW pyfb_direction AS'
        ' SELECT row_number() OVER () AS id, * FROM ('
        '  SELECT'
        '  p.prefix,'
        '  p.destination_id,'
        '  d.name AS destination_name,'
        '  d.carrier_id,'
        '  ca.name AS carrier_name,'
        '  d.country_iso2_id,'
        '  d.type_id,'
        '  t.name AS type_name,'
        '  c.region_id,'
        '  r.name AS region_name '
        'FROM pyfb_direction_prefix p '
        'LEFT JOIN pyfb_direction_destination d'
        '  ON d.id = p.destination_id '
        'LEFT JOIN pyfb_direction_carrier ca'
        '  ON ca.id = d.carrier_id '
        'LEFT JOIN pyfb_direction_type t'
        '  ON t.id = d.type_id '
        'LEFT JOIN pyfb_direction_country c'
        ' ON c.country_iso2 = d.country_iso2_id '
        'LEFT JOIN pyfb_direction_region r'
        '  ON r.id = c.region_id) v;'
        '',  # forward sql
        reverse_sql='DROP VIEW IF EXISTS dialplan CASCADE; ',  # sql for removal
    ),
]

# DROP VIEW IF EXISTS pyfb_direction CASCADE; CREATE OR REPLACE VIEW pyfb_direction AS SELECT row_number() OVER () AS id, * FROM ( SELECT p.prefix, p.destination_id, d.name AS destination_name, d.carrier_id, ca.name AS carrier_name, d.country_iso2_id, d.type_id, t.name AS type_name, c.region_id, r.name AS region_name FROM pyfb_direction_prefix p LEFT JOIN pyfb_direction_destination d ON d.id = p.destination_id LEFT JOIN pyfb_direction_carrier ca ON ca.id = d.carrier_id LEFT JOIN pyfb_direction_type t ON t.id = d.type_id LEFT JOIN pyfb_direction_country c ON c.country_iso2 = d.country_iso2_id LEFT JOIN pyfb_direction_region r ON r.id = c.region_id) v;
