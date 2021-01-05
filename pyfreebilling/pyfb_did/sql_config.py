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
        '  ud.domain AS domain '
        'FROM pyfb_did_routes dr '
        'LEFT JOIN pyfb_did d '
        ' ON dr.contract_did_id = d.id AND dr.type = \'s\' '
        'LEFT JOIN pyfb_endpoint_customer cd'
        '  ON dr.trunk_id = cd.id '
        'LEFT JOIN domain ud'
        '  ON ud.id = cd.domain_id;'
        '',  # forward sql
        reverse_sql='DROP VIEW IF EXISTS dbaliases CASCADE;',  # sql for removal
    ),
]

# DROP VIEW IF EXISTS custrates CASCADE; CREATE OR REPLACE VIEW custrates AS
# SELECT row_number() OVER () AS id, * FROM (
# SELECT r.id AS ratecard_id, 1 AS rate_type, r.name AS ratecard_name, r.rc_type, pr.status, r_rate, r_block_min_duration, r_minimal_time, r_init_block, prefix, destnum_length, CAST(null AS int) AS destination_id, CAST(null AS int) AS country_id, CAST(null AS int) AS type_id, CAST(null AS int) AS region_id FROM pyfb_rating_c_ratecard r
# JOIN pyfb_rating_c_prefix_rate pr ON pr.c_ratecard_id = r.id  AND pr.status <> 'disabled'
# WHERE r.status = 'enabled' AND now() > r.date_start AND now() < r.date_end
# UNION ALL
# SELECT r.id AS ratecard_id, 2 AS rate_type, r.name AS ratecard_name, r.rc_type, dr.status, r_rate, r_block_min_duration, r_minimal_time, r_init_block, CAST(null AS varchar) AS prefix, 0 AS destnum_length, destination_id, CAST(null AS int) AS country_id, CAST(null AS int) AS type_id, CAST(null AS int) AS region_id FROM pyfb_rating_c_ratecard r
# JOIN pyfb_rating_c_destination_rate dr ON dr.c_ratecard_id = r.id  AND dr.status <> 'disabled'
# WHERE r.status = 'enabled' AND now() > r.date_start AND now() < r.date_end
# UNION ALL
# SELECT r.id AS ratecard_id, 3 AS rate_type, r.name AS ratecard_name, r.rc_type, ctr.status, r_rate, r_block_min_duration, r_minimal_time, r_init_block, CAST(null AS varchar) AS prefix, 0 AS destnum_length, CAST(null AS int) AS destination_id, country_id, type_id, CAST(null AS int) AS region_id FROM pyfb_rating_c_ratecard r
# JOIN pyfb_rating_c_countrytype_rate ctr ON ctr.c_ratecard_id = r.id  AND ctr.status <> 'disabled'
# WHERE r.status = 'enabled' AND now() > r.date_start AND now() < r.date_end
# UNION ALL
# SELECT r.id AS ratecard_id, 4 AS rate_type, r.name AS ratecard_name, r.rc_type, cr.status, r_rate, r_block_min_duration, r_minimal_time, r_init_block, CAST(null AS varchar) AS prefix, 0 AS destnum_length, CAST(null AS int) AS destination_id, country_id, CAST(null AS int) AS type_id, CAST(null AS int) AS region_id FROM pyfb_rating_c_ratecard r
# JOIN pyfb_rating_c_country_rate cr ON cr.c_ratecard_id = r.id  AND cr.status <> 'disabled'
# WHERE r.status = 'enabled' AND now() > r.date_start AND now() < r.date_end
# UNION ALL
# SELECT r.id AS ratecard_id, 5 AS rate_type, r.name AS ratecard_name, r.rc_type, rtr.status, r_rate, r_block_min_duration, r_minimal_time, r_init_block, CAST(null AS varchar) AS prefix, 0 AS destnum_length, CAST(null AS int) AS destination_id, CAST(null AS int) AS country_id, type_id, region_id FROM pyfb_rating_c_ratecard r
# JOIN pyfb_rating_c_regiontype_rate rtr ON rtr.c_ratecard_id = r.id  AND rtr.status <> 'disabled'
# WHERE r.status = 'enabled' AND now() > r.date_start AND now() < r.date_end
# UNION ALL
# SELECT r.id AS ratecard_id, 6 AS rate_type, r.name AS ratecard_name, r.rc_type, rr.status, r_rate, r_block_min_duration, r_minimal_time, r_init_block, CAST(null AS varchar) AS prefix, 0 AS destnum_length, CAST(null AS int) AS destination_id, CAST(null AS int) AS country_id, CAST(null AS int) AS type_id, region_id FROM pyfb_rating_c_ratecard r
# JOIN pyfb_rating_c_region_rate rr ON rr.c_ratecard_id = r.id  AND rr.status <> 'disabled'
# WHERE r.status = 'enabled' AND now() > r.date_start AND now() < r.date_end
# UNION ALL
# SELECT r.id AS ratecard_id, 7 AS rate_type, r.name AS ratecard_name, r.rc_type, dr.status, r_rate, r_block_min_duration, r_minimal_time, r_init_block, CAST(null AS varchar) AS prefix, 0 AS destnum_length, CAST(null AS int) AS destination_id, CAST(null AS int) AS country_id, CAST(null AS int) AS type_id, CAST(null AS int) AS region_id FROM pyfb_rating_c_ratecard r
# JOIN pyfb_rating_c_default_rate dr ON dr.c_ratecard_id = r.id  AND dr.status <> 'disabled'
# WHERE r.status = 'enabled' AND now() > r.date_start AND now() < r.date_end
# )v;
