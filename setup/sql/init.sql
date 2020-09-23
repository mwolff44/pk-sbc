-- FUNCTION: public.create_cdr()

-- DROP FUNCTION public.create_cdr();

CREATE FUNCTION public.create_cdr()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
DECLARE

r RECORD;
rate NUMERIC := 0.0;
block_min_duration INTEGER := 0;
minimal_time INTEGER := 0;
init_block NUMERIC := 0.0;
o_total_sell NUMERIC := 0;
t_total_sell NUMERIC := 0;
o_total_cost NUMERIC := 0;
t_total_cost NUMERIC := 0;
o_rate NUMERIC := 0;
t_rate NUMERIC := 0;
o_cost_rate NUMERIC := 0;
t_cost_rate NUMERIC := 0;
o_billsec INTEGER := 0;
o_costsec INTEGER := 0;
t_billsec INTEGER := 0;
t_costsec INTEGER := 0;

BEGIN

    -- get rate

IF NEW.o_c_rate_id > 0 THEN
  CASE NEW.o_c_rate_type
    WHEN 1 THEN 
    EXECUTE 'SELECT r_rate, r_block_min_duration, r_minimal_time, r_init_block  
      FROM pyfb_rating_c_prefix_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.o_c_rate_id;
    WHEN 2 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_c_destination_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.o_c_rate_id;
    WHEN 3 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_c_countrytype_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.o_c_rate_id;
    WHEN 4 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_c_country_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.o_c_rate_id;
    WHEN 5 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_c_regiontype_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.o_c_rate_id;
    WHEN 6 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_c_region_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.o_c_rate_id;
    WHEN 7 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_c_default_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.o_c_rate_id;
  END CASE;

  IF NEW.duration < block_min_duration THEN o_billsec := block_min_duration;
  ELSE
    o_billsec := CEILING(NEW.duration / block_min_duration) * block_min_duration;
  END IF;
  o_total_sell := round((rate * o_billsec / 60.0 + init_block), 6);
  o_rate := rate;
END IF;

IF NEW.t_c_rate_id > 0 THEN
  CASE NEW.t_c_rate_type
    WHEN 1 THEN 
    EXECUTE 'SELECT r_rate, r_block_min_duration, r_minimal_time, r_init_block  
      FROM pyfb_rating_c_prefix_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.t_c_rate_id;
    WHEN 2 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_c_destination_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.t_c_rate_id;
    WHEN 3 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_c_countrytype_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.t_c_rate_id;
    WHEN 4 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_c_country_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.t_c_rate_id;
    WHEN 5 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_c_regiontype_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.t_c_rate_id;
    WHEN 6 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_c_region_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.t_c_rate_id;
    WHEN 7 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_c_default_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.t_c_rate_id;
  END CASE;

  IF NEW.duration < block_min_duration THEN t_billsec := block_min_duration;
  ELSE
    t_billsec := CEILING(NEW.duration / block_min_duration) * block_min_duration;
  END IF;
  t_total_sell := round((rate * t_billsec / 60.0 + init_block), 6);
  t_rate := rate;
END IF;

IF NEW.o_p_rate_id > 0 THEN
  CASE NEW.o_p_rate_type
    WHEN 1 THEN 
    EXECUTE 'SELECT r_rate, r_block_min_duration, r_minimal_time, r_init_block  
      FROM pyfb_rating_p_prefix_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.o_p_rate_id;
    WHEN 2 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_p_destination_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.o_p_rate_id;
    WHEN 3 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_p_countrytype_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.o_p_rate_id;
    WHEN 4 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_p_country_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.o_p_rate_id;
    WHEN 5 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_p_regiontype_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.o_p_rate_id;
    WHEN 6 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_p_region_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.o_p_rate_id;
    WHEN 7 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_p_default_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.o_p_rate_id;
  END CASE;

  IF NEW.duration < block_min_duration THEN o_costsec := block_min_duration;
  ELSE
    o_costsec := CEILING(NEW.duration / block_min_duration) * block_min_duration;
  END IF;
  o_total_cost := round((rate * o_costsec / 60.0 + init_block), 6);
  o_cost_rate := rate;
END IF;

IF NEW.t_p_rate_id > 0 THEN
    CASE NEW.t_p_rate_type
    WHEN 1 THEN 
    EXECUTE 'SELECT r_rate, r_block_min_duration, r_minimal_time, r_init_block  
      FROM pyfb_rating_p_prefix_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.t_p_rate_id;
    WHEN 2 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_p_destination_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.t_p_rate_id;
    WHEN 3 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_p_countrytype_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.t_p_rate_id;
    WHEN 4 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_p_country_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.t_p_rate_id;
    WHEN 5 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_p_regiontype_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.t_p_rate_id;
    WHEN 6 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_p_region_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.t_p_rate_id;
    WHEN 7 THEN 
    EXECUTE 'SELECT r_rate AS rate, r_block_min_duration AS block_min_duration, r_minimal_time AS minimal_time, r_init_block AS init_block 
      FROM pyfb_rating_p_default_rate WHERE id = $1' INTO rate, block_min_duration, minimal_time, init_block USING NEW.t_p_rate_id;
  END CASE;

  IF NEW.duration < block_min_duration THEN t_costsec := block_min_duration;
  ELSE
    t_costsec := CEILING(NEW.duration / block_min_duration) * block_min_duration;
  END IF;
  t_total_cost := round((rate * t_costsec / 60.0 + init_block), 6);
  t_cost_rate := rate;
END IF;

	-- inbound call delivered to customer
	IF NEW.term_customer!= 0 and NEW.orig_provider !=0 AND NEW.term_provider = 0 AND NEW.orig_customer = 0 then

	INSERT INTO pyfb_reporting_cdr(id, customer_ip, aleg_uuid, caller_number, callee_number, start_time, answered_time, end_time, duration, sip_code, sip_reason, sip_charge_info, sip_rtp_rxstat, sip_rtp_txstat, kamailio_server, direction, callee_destination_id, caller_destination_id, customer_id, provider_id, media_server_id, call_class, cdr_acc_id, billsec, costsec, total_sell, total_cost, cost_rate, rate, read_codec, write_codec, sip_user_agent, hangup_disposition, rated)
      VALUES (gen_random_uuid(), '', NEW.callid, NEW.e164_caller, NEW.e164_called, NEW.start_time, NEW.answered_time, NEW.end_time, NEW.duration, coalesce(NEW.sip_code,''), coalesce(NEW.sip_reason, ''), coalesce(NEW.sip_charge_info, ''), coalesce(NEW.sip_rtp_rxstat, '0'), coalesce(NEW.sip_rtp_txstat, '0'), NEW.kamailio_server, NEW.direction, NEW.called_destination, NEW.caller_destination, NEW.term_customer, NEW.orig_provider, NEW.media_server, NEW.leg_a_class, new.ID, t_billsec, o_costsec, t_total_sell, o_total_cost, o_cost_rate, t_rate, '', '', '', '', current_timestamp);
	UPDATE acc_cdrs SET processed = current_timestamp WHERE id = NEW.id;
	
	-- outbound call delivered to provider
	ELSIF NEW.orig_customer!= 0 and NEW.term_provider !=0 AND NEW.orig_provider = 0 AND NEW.term_customer = 0then

	INSERT INTO pyfb_reporting_cdr(id, customer_ip, aleg_uuid, caller_number, callee_number, start_time, answered_time, end_time, duration, sip_code, sip_reason, sip_charge_info, sip_rtp_rxstat, sip_rtp_txstat, kamailio_server, direction, callee_destination_id, caller_destination_id, customer_id, provider_id, media_server_id, call_class, cdr_acc_id, billsec, costsec, total_sell, total_cost, cost_rate, rate, read_codec, write_codec, sip_user_agent, hangup_disposition, rated)
      VALUES (gen_random_uuid(), '', NEW.callid, NEW.e164_caller, NEW.e164_called, NEW.start_time, NEW.answered_time, NEW.end_time, NEW.duration, coalesce(NEW.sip_code,''), coalesce(NEW.sip_reason, ''), coalesce(NEW.sip_charge_info, ''), coalesce(NEW.sip_rtp_rxstat, '0'), coalesce(NEW.sip_rtp_txstat, '0'), NEW.kamailio_server, NEW.direction, NEW.called_destination, NEW.caller_destination, NEW.orig_customer, NEW.term_provider, NEW.media_server, NEW.leg_a_class, new.ID, o_billsec, t_costsec, o_total_sell, t_total_cost, t_cost_rate, o_rate, '', '', '', '', current_timestamp);
	UPDATE acc_cdrs SET processed = current_timestamp WHERE id = NEW.id;
	
	-- inbound call forwarded to outside number
	-- we need to CDR, one for the leg A and one for the leg B
	ELSIF NEW.orig_provider!= 0 and NEW.term_provider !=0 then

	INSERT INTO pyfb_reporting_cdr(id, customer_ip, aleg_uuid, caller_number, callee_number, start_time, answered_time, end_time, duration, sip_code, sip_reason, sip_charge_info, sip_rtp_rxstat, sip_rtp_txstat, kamailio_server, direction, callee_destination_id, caller_destination_id, customer_id, provider_id, media_server_id, call_class, cdr_acc_id, billsec, costsec, total_sell, total_cost, cost_rate, rate, read_codec, write_codec, sip_user_agent, hangup_disposition, rated)
      VALUES (gen_random_uuid(), '', NEW.callid, NEW.e164_caller, NEW.called_did, NEW.start_time, NEW.answered_time, NEW.end_time, NEW.duration, coalesce(NEW.sip_code,''), coalesce(NEW.sip_reason, ''), coalesce(NEW.sip_charge_info, ''), coalesce(NEW.sip_rtp_rxstat, '0'), coalesce(NEW.sip_rtp_txstat, '0'), NEW.kamailio_server, NEW.direction, NEW.did_destination, NEW.caller_destination, NEW.term_customer, NEW.orig_provider, NEW.media_server, NEW.leg_a_class, new.ID, t_billsec, o_costsec, t_total_sell, o_total_cost, o_cost_rate, t_rate, '', '', '', '', current_timestamp),
	         (gen_random_uuid(), '', NEW.callid, NEW.called_did, NEW.e164_called, NEW.start_time, NEW.answered_time, NEW.end_time, NEW.duration, coalesce(NEW.sip_code,''), coalesce(NEW.sip_reason, ''), coalesce(NEW.sip_charge_info, ''), coalesce(NEW.sip_rtp_rxstat, '0'), coalesce(NEW.sip_rtp_txstat, '0'), NEW.kamailio_server, 'outbound', NEW.called_destination, NEW.did_destination, NEW.term_customer, NEW.term_provider, NEW.media_server, NEW.leg_b_class, new.ID, o_billsec, t_costsec, o_total_sell, t_total_cost, t_cost_rate, o_rate, '', '', '', '', current_timestamp);
	UPDATE acc_cdrs SET processed = current_timestamp WHERE id = NEW.id;
	
	END IF;
	
	RETURN NULL;
END;
$BODY$;

ALTER FUNCTION public.create_cdr()
    OWNER TO pyfreebilling;

