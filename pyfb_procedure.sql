CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE OR REPLACE FUNCTION public.create_cdr() 
  RETURNS TRIGGER
  LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
BEGIN
	-- inbound call delivered to customer
	IF NEW.term_customer!= 0 and NEW.orig_provider !=0 AND NEW.term_provider = 0 AND NEW.orig_customer = 0 then

	INSERT INTO pyfb_reporting_cdr(id, customer_ip, aleg_uuid, caller_number, callee_number, start_time, answered_time, end_time, duration, sip_code, sip_reason, sip_charge_info, sip_rtp_rxstat, sip_rtp_txstat, kamailio_server, direction, callee_destination_id, caller_destination_id, customer_id, provider_id, media_server_id, call_class, cdr_acc_id, billsec, total_sell, total_cost, cost_rate, rate, read_codec, write_codec, sip_user_agent, hangup_disposition)
      VALUES (gen_random_uuid() returns uuid, '', NEW.callid, NEW.e164_caller, NEW.e164_called, NEW.start_time, NEW.answered_time, NEW.end_time, NEW.duration, coalesce(NEW.sip_code,''), coalesce(NEW.sip_reason, ''), coalesce(NEW.sip_charge_info, ''), coalesce(NEW.sip_rtp_rxstat, '0'), coalesce(NEW.sip_rtp_txstat, '0'), NEW.kamailio_server, NEW.direction, NEW.called_destination, NEW.caller_destination, NEW.term_customer, NEW.orig_provider, NEW.media_server, NEW.leg_a_class, new.ID, 0, 0, 0, 0, 0, '', '', '', '');
	UPDATE acc_cdrs SET processed = current_timestamp WHERE id = NEW.id;
	
	-- outbound call delivered to provider
	ELSIF NEW.orig_customer!= 0 and NEW.term_provider !=0 AND NEW.orig_provider = 0 AND NEW.term_customer = 0then

	INSERT INTO pyfb_reporting_cdr(id, customer_ip, aleg_uuid, caller_number, callee_number, start_time, answered_time, end_time, duration, sip_code, sip_reason, sip_charge_info, sip_rtp_rxstat, sip_rtp_txstat, kamailio_server, direction, callee_destination_id, caller_destination_id, customer_id, provider_id, media_server_id, call_class, cdr_acc_id, billsec, total_sell, total_cost, cost_rate, rate, read_codec, write_codec, sip_user_agent, hangup_disposition)
      VALUES (gen_random_uuid() returns uuid, '', NEW.callid, NEW.e164_caller, NEW.e164_called, NEW.start_time, NEW.answered_time, NEW.end_time, NEW.duration, coalesce(NEW.sip_code,''), coalesce(NEW.sip_reason, ''), coalesce(NEW.sip_charge_info, ''), coalesce(NEW.sip_rtp_rxstat, '0'), coalesce(NEW.sip_rtp_txstat, '0'), NEW.kamailio_server, NEW.direction, NEW.called_destination, NEW.caller_destination, NEW.orig_customer, NEW.term_provider, NEW.media_server, NEW.leg_a_class, new.ID, 0, 0, 0, 0, 0, '', '', '', '');
	UPDATE acc_cdrs SET processed = current_timestamp WHERE id = NEW.id;
	
	-- inbound call forwarded to outside number
	-- we need to CDR, one for the leg A and one for the leg B
	ELSIF NEW.orig_provider!= 0 and NEW.term_provider !=0 then

	INSERT INTO pyfb_reporting_cdr(id, customer_ip, aleg_uuid, caller_number, callee_number, start_time, answered_time, end_time, duration, sip_code, sip_reason, sip_charge_info, sip_rtp_rxstat, sip_rtp_txstat, kamailio_server, direction, callee_destination_id, caller_destination_id, customer_id, provider_id, media_server_id, call_class, cdr_acc_id, billsec, total_sell, total_cost, cost_rate, rate, read_codec, write_codec, sip_user_agent, hangup_disposition)
      VALUES (gen_random_uuid() returns uuid, '', NEW.callid, NEW.e164_caller, NEW.called_did, NEW.start_time, NEW.answered_time, NEW.end_time, NEW.duration, coalesce(NEW.sip_code,''), coalesce(NEW.sip_reason, ''), coalesce(NEW.sip_charge_info, ''), coalesce(NEW.sip_rtp_rxstat, '0'), coalesce(NEW.sip_rtp_txstat, '0'), NEW.kamailio_server, NEW.direction, NEW.did_destination, NEW.caller_destination, NEW.term_customer, NEW.orig_provider, NEW.media_server, NEW.leg_a_class, new.ID, 0, 0, 0, 0, 0, '', '', '', ''),
	         (gen_random_uuid() returns uuid, '', NEW.callid, NEW.called_did, NEW.e164_called, NEW.start_time, NEW.answered_time, NEW.end_time, NEW.duration, coalesce(NEW.sip_code,''), coalesce(NEW.sip_reason, ''), coalesce(NEW.sip_charge_info, ''), coalesce(NEW.sip_rtp_rxstat, '0'), coalesce(NEW.sip_rtp_txstat, '0'), NEW.kamailio_server, 'outbound', NEW.called_destination, NEW.did_destination, NEW.term_customer, NEW.term_provider, NEW.media_server, NEW.leg_b_class, new.ID, 0, 0, 0, 0, 0, '', '', '', '');
	UPDATE acc_cdrs SET processed = current_timestamp WHERE id = NEW.id;
	
	END IF;
	
	RETURN NULL;
END;
$BODY$;

CREATE TRIGGER new_cdr_trigger AFTER INSERT ON acc_cdrs
FOR EACH ROW EXECUTE PROCEDURE create_cdr()

 
-- rateing
// o_c_rate_id o_c_rate_type - id de 0 à 7 -
// 0 pas de rate
// 1 pyfb_rating_c_prefix_rate
// 2 pyfb_rating_c_destination_rate
// 3 pyfb_rating_c_countrytype_rate
// 4 pyfb_rating_c_country_rate
// 5 pyfb_rating_c_regiontype_rate
// 6 pyfb_rating_c_region_rate
// 7 pyfb_rating_c_default_rate
r_rate,
r_block_min_duration,
r_minimal_time,
r_init_block,

IF o_c_rate_id > 0 THEN
  SELECT r_rate AS o_c_rate, r_block_min_duration AS o_c_block_min_duration, r_minimal_time AS o_c_minimal_time, r_init_block AS o_c_init_block 
    FROM
      CASE
        WHERE o_c_rate_type = 1 THEN pyfb_rating_c_prefix_rate
        WHERE o_c_rate_type = 2 THEN pyfb_rating_c_destination_rate
        WHERE o_c_rate_type = 3 THEN pyfb_rating_c_countrytype_rate
        WHERE o_c_rate_type = 4 THEN pyfb_rating_c_country_rate
        WHERE o_c_rate_type = 5 THEN pyfb_rating_c_regiontype_rate
        WHERE o_c_rate_type = 6 THEN pyfb_rating_c_region_rate
        WHERE o_c_rate_type = 7 THEN pyfb_rating_c_default_rate
    WHERE id = o_c_rate_id;
END IF;

o_total_sell = 0
t_total_sell = 0
o_total_cost = 0
t_total_cost = 0
billsec = 0

Si rate_type > 0 alors requête pour les 4 type de companies

IF duration < block_min_duration
  THEN billsec = block_min_duration;
ELSE
  billsec = FLOOR(duration / block_min_duration) * block_min_duration;
END IF;

total_sell = round((r_rate * billsec / 60.0 + init_block), 6);





-- test


-- INCOMIN?G
INSERT INTO public.acc_cdrs(
	id, start_time, end_time, duration, callee, caller, callid, direction, answered_time, called_destination, called_did, caller_destination, did_destination, e164_called, e164_caller, kamailio_server, leg_a_class, leg_b_class, media_server, o_c_rate_id, o_c_rate_type, o_p_rate_id, o_p_rate_type, orig_customer, orig_provider, sip_charge_info, sip_code, sip_reason, sip_rtp_rxstat, sip_rtp_txstat, sip_user_agent, t_c_rate_id, t_c_rate_type, t_p_rate_id, t_p_rate_type, term_customer, term_provider, processed)
	VALUES (56, '2020-05-27 21:05:55+02', '2020-05-27 21:05:55+02', 0.655, '33493879019', '33465630506', '1461253838-5855@SVIGateway', 'inbound', NULL, 3, '33493879019', 3, 3, '33493879019', '33465630506', 1, 'on-net', 'on-net', NULL, 0, 0, 0, 0, 0, 1, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, 0, 2, 0, NULL);

-- OUTGOING
INSERT INTO public.acc_cdrs(
	id, start_time, end_time, duration, callee, caller, callid, direction, answered_time, called_destination, called_did, caller_destination, did_destination, e164_called, e164_caller, kamailio_server, leg_a_class, leg_b_class, media_server, o_c_rate_id, o_c_rate_type, o_p_rate_id, o_p_rate_type, orig_customer, orig_provider, sip_charge_info, sip_code, sip_reason, sip_rtp_rxstat, sip_rtp_txstat, sip_user_agent, t_c_rate_id, t_c_rate_type, t_p_rate_id, t_p_rate_type, term_customer, term_provider, processed)
	VALUES (57, '2020-05-27 21:05:55+02', '2020-05-27 21:05:55+02', 10.655, '33367674713', '33493879019', 'd1e415dz-dz14511', 'outbound', NULL, 3, '0', 3, NULL, '33367674713', '33493879019', 1, 'off-net', 'off-net', NULL, 0, 0, 0, 0, 3, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 1, 7, 0, 1, NULL);

-- inbound call forwarded
INSERT INTO public.acc_cdrs(
	id, start_time, end_time, duration, callee, caller, callid, direction, answered_time, called_destination, called_did, caller_destination, did_destination, e164_called, e164_caller, kamailio_server, leg_a_class, leg_b_class, media_server, o_c_rate_id, o_c_rate_type, o_p_rate_id, o_p_rate_type, orig_customer, orig_provider, sip_charge_info, sip_code, sip_reason, sip_rtp_rxstat, sip_rtp_txstat, sip_user_agent, t_c_rate_id, t_c_rate_type, t_p_rate_id, t_p_rate_type, term_customer, term_provider, processed)
	VALUES (58, '2020-05-27 21:05:55+02', '2020-05-27 21:05:55+02', 30.655, '33146542793', '33608728270', 'd1e415dz-dz14511@SVI', 'inbound', NULL, 3, '33146542793', 1, 3, '33155581700', '33608728270', 1, 'on-net', 'off-net', NULL, 0, 0, 0, 0, 0, 1, NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 1, 7, 2, 1, NULL);



