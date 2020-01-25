insert into pyfb_company(name, slug, created, modified, address, contact_name, contact_phone)
SELECT(
	SELECT concat_ws(' ',name_first, name_last) as generated
	FROM (
		SELECT string_agg(x,'')
		FROM (
			select start_arr[ 1 + ( (random() * 25)::int) % 16 ]
			FROM
			(
			    select '{CO,GE,FOR,SO,CO,GIM,SE,CO,GE,CA,FRA,GEC,GE,GA,FRO,GIP}'::text[] as start_arr
			) syllarr,
			-- need 3 syllabes, and force generator interpretation with the '*0' (else 3 same syllabes)
			generate_series(1, 3 + (generator*0))
		) AS comp3syl(x)
	) AS comp_name_1st(name_first),
	(
		SELECT x[ 1 + ( (random() * 25)::int) % 14 ]
		FROM (		
			select '{Ltd,& Co,SARL,SA,Gmbh,United,Brothers,& Sons,International,Ext,Worldwide,Global,2000,3000}'::text[]
		) AS z2(x)
	) AS comp_name_last(name_last)
    ) as name,
    generator as slug,
    current_timestamp as created,
    current_timestamp as modified,
    '' as address,
    '' as contact_name,
    '' as contact_phone
FROM generate_series(1,10000) as generator
-- ignore duplicates company names
ON CONFLICT DO nothing;


