--# Copyright 2013 Mathias WOLFF
--# This file is part of pyfreebilling.
--#
--# pyfreebilling is free software: you can redistribute it and/or modify
--# it under the terms of the GNU General Public License as published by
--# the Free Software Foundation, either version 3 of the License, or
--# (at your option) any later version.
--#
--# pyfreebilling is distributed in the hope that it will be useful,
--# but WITHOUT ANY WARRANTY; without even the implied warranty of
--# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
--# GNU General Public License for more details.
--#
--# You should have received a copy of the GNU General Public License
--# along with pyfreebilling.  If not, see <http://www.gnu.org/licenses/>

-----------------------------------------------
--        WHOLESALE SCRIPT
-----------------------------------------------

-----------------------------------------------
-----------------------------------------------
--        FUNCTIONS
-----------------------------------------------
-----------------------------------------------

-----------------------------------------------
-----------------------------------------------
--        HANGUP
-----------------------------------------------
-----------------------------------------------
function myHangupHook(s, status, arg)
  obCause = session:hangupCause()
  log("Hangup cause : ", obCause)
  exit()
end

-----------------------------------------------
-----------------------------------------------
--        LOG
-----------------------------------------------
-----------------------------------------------
function log(name, logval, level, getvar)
  local level = "warning"
  local getvar = getvar or "0"
  if channel["cli_debug"] == "True" or channel["cli_debug"] == "true" then
    if getvar == "0" then
      freeswitch.consoleLog(level, "------->" .. channel["uuid"] .. " - WS CALL " .. name .. ".....: " .. tostring(logval) .. "<-------------\n")
    else
      freeswitch.consoleLog(level, "-------> uuid is null - WS CALL " .. name .. ".....: " .. tostring(logval) .. "<-------------\n")
    end
  end
end
-----------------------------------------------
-----------------------------------------------
--        GRAB SESSION VARIABLES
-----------------------------------------------
-----------------------------------------------
function get_Variable(call_var)
  local value = session:getVariable(call_var)
  if value then
    log("Got value : ", call_var .. "  :  " .. tostring(value), "debug", 1)
  else
    log("Variable : not set ", call_var, "debug", 1)
  end

  return value
end
-----------------------------------------------
-----------------------------------------------
--        SET SESSION VARIABLES
-----------------------------------------------
-----------------------------------------------
function set_variable(call_var, value, default)
  local message
  if value then
    message = "Set value :"
  else
    value = default
    message = "Set value to default: "
  end
  session:setVariable(call_var, value)
  log(message, call_var.." "..tostring(value), "debug")
end
-----------------------------------------------
-----------------------------------------------
--        EXECUTE DIALPLAN APP
-----------------------------------------------
-----------------------------------------------
function execute(application, data)
  local application = application
  local data = data or ""
  if application then
    log("Executing dialplan application : ", application.." - "..data)
    session:execute(application, data)
  end
end
-----------------------------------------------
-----------------------------------------------
--        CALLER PRIVACY HEADER
-----------------------------------------------
-----------------------------------------------
function set_privacy(privacy)
  if privacy then
    set_variable("cid_type", "none")
    set_variable("sip_h_Privacy", "id")
  else
    set_variable("cid_type", "none")
    set_variable("sip_h_Privacy", "none")
  end
end
-----------------------------------------------
-----------------------------------------------
--        VOICEMAIL DETECTION
-----------------------------------------------
-----------------------------------------------
function onInput(session, type, obj)
  if type == "dtmf" and obj['digit'] == '1' and human_detected == false then
    execute("avmd", "stop")
    log("AVMD : ", "human detected", "debug")
    return "break"
  end

  if type == "event" and voicemail_detected == false then
    execute("avmd", "stop")
    log("AVMD : ", "voicemail detected", "debug")
    execute("curl", "http://1.1.1.1/v4/lib/sip_repondeur.php?dest="..channel["destination_number"])
    set_variable("proto_specific_hangup_cause", "PFB_VMD_DETECTED")
    session:hangup("NORMAL_CLEARING")
  end
end
-----------------------------------------------
-----------------------------------------------
function SessionHangupHook(s, status, arg)
  freeswitch.consoleLog("INFO", "wholesale: Call ended! " .. status .. "\n")
  assert(dbh:release())
end
-----------------------------------------------
-----------------------------------------------
local function sv(key, val)
  if session then
    session:setVariable(key, val)
  elseif stream then
    stream:write(string.format("%25s : %s\n", key, val))
  else -- a script executed using luarun does not have a stream
    print(key .. " : " .. val)
  end
end
-----------------------------------------------
-----------------------------------------------
function hangup_call(code, phrase, cause)
  assert(dbh:release())
  session:hangup()
end
-----------------------------------------------
-----------------------------------------------
function codec_test(type)
  local codecs = { "G729", "PCMA", "PCMU", "G722" }
  local codec_status = "NOK"
  log("customer codec test", "--start--", "info")
  for key, value in ipairs(codecs) do
    log("codecs_customer: ", channel["customer_codecs"], "info")
    log("codec value test: ", value, "debug")
    if string.find(channel["customer_codecs"], string.format("%s", value)) then
      if string.find(string.upper(channel["ep_codec_string"]), string.format("%s", value)) then
        log("codec leg A match with customer codec: ", value, "info")
        codec_status = "OK"
        log("codec status: ", codec_status, "info")
      else
        log("codec leg A mismatch with customer codec: ", value,"info")
        channel["customer_codecs"] = string.gsub(channel["customer_codecs"], string.format("%s%s", ",", value), "", 1)
        channel["customer_codecs"] = string.gsub(channel["customer_codecs"], string.format("%s%s", value, ","), "", 1)
        channel["customer_codecs"] = string.gsub(channel["customer_codecs"], string.format("%s", value), "", 1)
        log("New customer codec list available : ", channel["customer_codecs"], "info")
      end
    else
      log("codec not available for this sip account: ", value, "info")
    end
  end
  if codec_status == "OK" then
    log("codec leg A match with customer codec", "", "info")
    log("codec available : ", channel["customer_codecs"], "info")
    execute("export", "nolocal:absolute_codec_string="..channel["customer_codecs"])
  else
    set_variable("proto_specific_hangup_cause", "PFB_CUSTOMER_CODEC_ERROR")
    log("codec leg A mismatch with customer codec! ","Exiting","info")
    session:hangup("BEARERCAPABILITY_NOTAVAIL")
    return
  end
end
-----------------------------------------------
-----------------------------------------------
--        SCRIPT START
-----------------------------------------------
-----------------------------------------------
-----------------------------------------------
--        GET CHANNEL VARIABLES
-----------------------------------------------
--session:execute("info", "")
--session:setHangupHook("myHangupHook")
channel = {}
pyfb_caller_id_number = ""
if session:ready() then
  channel["cli_debug"] = "True"
  channel["uuid"] = get_Variable("uuid")
  channel["context"] = get_Variable("context")
  channel["sipaccountcode"] = get_Variable("sip_h_X-PyFB-AccountId")
  channel["call-type"] = get_Variable("sip_h_X-PyFB-CallType")
  channel["user_name"] = get_Variable("user_name")
  channel["sip_authorized"] = get_Variable("sip_authorized")
  channel["destination_number"] = get_Variable("destination_number")
  channel["caller_id_number"] = get_Variable("sip_h_X-PyFB-CallerNum")
  channel["caller_id_name"] = get_Variable("caller_id_name")
  channel["direction"] = get_Variable("direction")
  channel["session_id"] = get_Variable("session_id")
  channel["sip_from_user"] = get_Variable("sip_from_user")
  channel["kam_received_ip"] = get_Variable("sip_received_ip")
  channel["sip_received_ip"] = get_Variable("sip_h_X-AUTH-IP")
  channel["sip_acl_authed_by"] = get_Variable("sip_acl_authed_by")
  channel["sip_network_ip"] = get_Variable("sip_network_ip")
  channel["auth_acl"] = get_Variable("auth_acl")
  channel["sip_user_agent"] = get_Variable("sip_user_agent")
  channel["vmd"] = "false"
  channel["internal_kam_ip"] = freeswitch.getGlobalVariable("internal_kam_ip")
  log("Got value : ", "internal_kam_ip  :  " .. channel["internal_kam_ip"], "debug", 1)
  channel["external_kam_ip"] = freeswitch.getGlobalVariable("external_kam_ip")
  log("Got value : ", "external_kam_ip  :  " .. channel["external_kam_ip"], "debug", 1)

  if channel["sip_user_agent"] then
    log("sip_user_agent :", "is OK", "debug")
  else
    channel["sip_user_agent"] = "not set"
  end
--  channel["FreeSWITCH-IPv4"] = get_Variable("FreeSWITCH-IPv4")
--  channel["FreeSWITCH-Switchname"] = get_Variable("FreeSWITCH-Switchname")
  log("Get session variable :", "done", "debug")
  
  -- Clean + in callerID
  pyfb_caller_id_number = string.gsub(channel["caller_id_number"], "+", "", 1)
  log("CallerID num", " - clean plus sign : " .. pyfb_caller_id_number, "debug", 1)
  -- Clean non alphanum in callerID
  if tonumber(pyfb_caller_id_number) then
      log("CallerID num", " - clean only digits ", "debug", 1)
  else
      pyfb_caller_id_number = "CALLERIDNONAVAIL"
      channel["caller_id_number"] = "Anonymous"
      log("CallerID num", " - clean alphanum : " .. pyfb_caller_id_number, "debug", 1)
  end
  
  set_variable("user_agent", channel["sip_user_agent"])
  set_variable("customer_ip", channel["sip_received_ip"])
  set_variable("cost_rate", "0.000000")
  set_variable("sell_rate", "0.000000")
  set_variable("init_block", "0.000000")
  set_variable("sell_increment", "0")
  set_variable("originating_leg_uuid", channel["uuid"])


  -----------------------------------------------
  --        CallType
  -----------------------------------------------
  if channel["call-type"] == "PSTN" then
      myprofile = "external"
      ratecardfilter = "AND rc.rctype = 'PSTN' "
  elseif channel["call-type"] == "DIDOUT" then
      myprofile = "internal"
      ratecardfilter = "AND ( rc.rctype = 'PSTN' OR rc.rctype = 'DIDOUT' ) "
  elseif channel["call-type"] == "DIDIN" then
      myprofile = "internal"
      ratecardfilter = "AND rc.rctype = 'DIDIN' "
  elseif channel["call-type"] == "EMERGENCY" then
      myprofile = "external"
      ratecardfilter = "AND rc.rctype = 'EMERGENCY' "
  else
      myprofile = "external"
  end
  log("ratecardfilter variable :", ratecardfilter, "debug")
  log("myprofile variable :", myprofile, "debug")

-----------------------------------------------
--        DATABASE CONNECTION
-----------------------------------------------
if session:ready() then
  if channel["sip_authorized"] then
    dbh = freeswitch.Dbh("odbc://freeswitch")
    if dbh:connected() == false then
      set_variable("proto_specific_hangup_cause", "PFB_DB_ERROR")
      log("Dbh : ", "Database error - Hangup call", "ERROR")
      session:hangup("BEARERCAPABILITY_NOTAVAIL")
      return
    else
      log("Dbh : ", "Database connected")
    end
  else
    log("Customer not authorized")
    set_variable("proto_specific_hangup_cause", "PFB_NOT_AUTH", "INFO")
    if dbh:connected() == true then
      log("DBH Connected : releasing","","debug")
      assert(dbh:release())
    end
    session:hangup("BEARERCAPABILITY_NOTAVAIL")
    return
  end
end
-----------------------------------------------
--        Get Wholesale Customer Settings
-----------------------------------------------
if session:ready() then
  if (channel["caller_id_number"] == nil or channel["caller_id_number"] =="") then
    channel["caller_id_number"] = "anonymous"
  end
  customer = {}
  custok = 0
  if channel["call-type"] == "DIDIN" then
      query_cust_sql = [[SELECT
          cc.name AS name,
          cc.prepaid AS prepaid,
          cc.credit_limit AS credit_limit,
          cc.customer_balance AS customer_balance,
          cc.max_calls AS max_calls,
          cc.id AS accountcode,
          cd.name AS sipname,
          cd.cli_debug,
          cd.fake_ring,
          cd.ignore_early_media,
          cd.codecs AS customer_codecs,
          cd.outbound_caller_id_number,
          cp.id AS provider,
          d.cust_ratecard_id AS cust_ratecard,
          d.prov_ratecard_id AS prov_ratecard
          FROM did d
          INNER JOIN Company cc
            ON cc.id = d.customer_id
              AND cc.customer_enabled = TRUE
          INNER JOIN Company cp
            ON cp.id = d.provider_id
              AND cp.supplier_enabled = TRUE
          INNER JOIN did_routes dr
            ON contract_did_id = d.id
          INNER JOIN customer_directory cd
            ON cd.company_id = cc.id
              AND cd.enabled = TRUE
              AND cd.id = dr.trunk_id
          WHERE ']] .. channel["destination_number"] .. [[' LIKE concat(d.number,'%')]]
  else
      query_cust_sql = [[SELECT
          c.name AS name,
          c.prepaid AS prepaid,
          c.credit_limit AS credit_limit,
          c.customer_balance AS customer_balance,
          c.max_calls AS max_calls,
          c.id AS accountcode,
          cd.cli_debug,
          cd.fake_ring,
          cd.ignore_early_media,
          cd.codecs AS customer_codecs,
          cd.outbound_caller_id_number,
          cnr.prefix AS prefix,
          cnr.remove_prefix AS remove_prefix,
          cnr.add_prefix AS add_prefix ,
          ccnr.remove_prefix AS ccnr_remove_prefix,
          ccnr.add_prefix AS ccnr_add_prefix,
          dnr.format_num AS dnr_format_num
          FROM company c
          INNER JOIN customer_directory cd
            ON cd.name = ']] .. channel["sipaccountcode"] .. [['
              AND cd.enabled = TRUE
          LEFT JOIN customer_norm_rules cnr
          ON cnr.company_id = c.id
              AND ']] .. channel["destination_number"] .. [[' LIKE concat(cnr.prefix,'%')
          LEFT JOIN customer_cid_norm_rules ccnr
          ON ccnr.company_id = c.id
              AND ']] .. channel["caller_id_number"] .. [[' LIKE concat(ccnr.prefix,'%')
          LEFT JOIN destination_norm_rules dnr
          ON ']] .. channel["destination_number"] .. [[' LIKE concat(dnr.prefix,'%')
          WHERE c.id=cd.company_id
              AND c.customer_enabled = TRUE]]
  end

  log("SQL: ", query_cust_sql, "debug")
  assert(dbh:query(query_cust_sql, function(row)
    for key, val in pairs(row) do
      customer[key] = val
    end
    custok = 1
  end))

  channel["accountcode"] = customer["accountcode"]
  set_variable("customer", channel["accountcode"])
  -- channel["cli_debug"] = customer["cli_debug"]
  channel["ignore_early_media"] = customer["ignore_early_media"]
  channel["fake_ring"] = customer["fake_ring"]
  channel["outbound_caller_id_number"] = customer["outbound_caller_id_number"]

  log("Customer data - num of records", custok, "debug")
  if custok == 0 then
    set_variable("proto_specific_hangup_cause", "PFB_CUSTOMER_NOT_FOUND")
    log("CUSTOMER NOT FOUND!","Exiting")
    session:hangup("BEARERCAPABILITY_NOTAVAIL")
  end
  log("Prepaid / Balance / Credit limit : ".. customer["prepaid"] .." /  ".. tonumber(customer["customer_balance"]) .." / " .. tonumber(customer["credit_limit"]),"")
else
  if dbh:connected() == true then
    log("DBH Connected : releasing","","debug")
    assert(dbh:release())
  end
end

-----------------------------------------------
--        CODECS
-----------------------------------------------

  channel["customer_codecs"] = customer["customer_codecs"]
  channel["ep_codec_string"] = get_Variable("ep_codec_string")
  if channel["ep_codec_string"] == nil then
    set_variable("proto_specific_hangup_cause", "PFB_CUSTOMER_CODEC_ERROR")
    log("codec leg A provides no codec! ","Exiting","info")
    session:hangup("BEARERCAPABILITY_NOTAVAIL")
    return
  end
  if (channel["customer_codecs"] == "ALL" or channel["customer_codecs"] == nil or channel["customer_codecs"] == "") then
    log("All client codecs", "", "debug")
  else
    log("specific customer codecs", "", "debug")
    codec_test("customer")
  end
end
------------------------------------------------

if (session:ready() == true) then
  if customer["prepaid"] == "0" then
    log("Customer...: postpaid","")
    if tonumber(customer["customer_balance"]) < tonumber(customer["credit_limit"]) then
      set_variable("proto_specific_hangup_cause", "PFB_CUSTOMER_POSTPAID_CREDIT_LIMIT")
      log("CUSTOMER " .. customer["name"] .. " has reach credit limit... rejecting","")
      session:hangup("BEARERCAPABILITY_NOTAVAIL");
    else
      log("Credit limit : ","OK")
    end
  elseif customer["prepaid"] == "1" then
    log("Customer...: prepaid","")
    if tonumber(customer["customer_balance"]) < 0 then
      set_variable("proto_specific_hangup_cause", "PFB_CUSTOMER_PREPAID_NO_MONEY")
      log("CUSTOMER " .. customer["name"] .. " has no money... rejecting","")
      session:hangup("BEARERCAPABILITY_NOTAVAIL")
    else
      log("balance : ","OK")
    end
  end
else
  if dbh:connected() == true then
    log("DBH Connected : releasing","","debug")
    assert(dbh:release())
  end
end
-----------------------------------------------
--        Customer Normalization
-----------------------------------------------
if (session:ready() == true) then
  -- Called Num normalization
  if (customer["remove_prefix"] == "" or customer["remove_prefix"] == nil) then
    customer["remove_prefix"]  = "^"
  end
  if customer["add_prefix"] == nil then
    customer["add_prefix"]  = ""
  end
  channel["destination_number"] = string.gsub(channel["destination_number"], customer["remove_prefix"], customer["add_prefix"], 1)
  set_variable("destination_number", channel["destination_number"])

   -- test format destination number
  if customer["dnr_format_num"] == nil then
    log("Not Destination Number format rule"," : continue","debug")
  else
    if string.match(channel["destination_number"],customer["dnr_format_num"]) == nil then
      set_variable("proto_specific_hangup_cause", "PFB_DESTINATION_NUMBER_WRONG_FORMAT")
      log("Destination number wrong format :","NOK!", "debug")
      session:hangup("UNALLOCATED_NUMBER")
    else
      log("Destination number well formated :","OK!")
    end
  end

  -- CallerID normalization

  if (channel["outbound_caller_id_number"] == "" or channel["outbound_caller_id_number"] == nil) then
     channel["outbound_caller_id_number"] = channel["caller_id_number"]
  else
     channel["caller_id_number"] = channel["outbound_caller_id_number"]
  end
  if (customer["ccnr_remove_prefix"] == "" or customer["ccnr_remove_prefix"] == nil) then
    customer["ccnr_remove_prefix"]  = "^"
  end
  if customer["ccnr_add_prefix"] == nil then
    customer["ccnr_add_prefix"]  = ""
  end
  if (channel["caller_id_number"] == "" or channel["caller_id_number"] == nil) then
    channel["caller_id_number"] = "anonymous"
  else
    channel["caller_id_number"] = string.gsub(channel["caller_id_number"], customer["ccnr_remove_prefix"], customer["ccnr_add_prefix"], 1)
    log("CallerID Norm - callerID num / rem_prefix / add_prefix : ", channel["caller_id_number"].." / "..customer["ccnr_remove_prefix"].." / "..customer["ccnr_add_prefix"], "debug")
  end
  pyfb_caller_id_number = string.gsub(channel["caller_id_number"], "+", "", 1)
  log("Customer CallerID : ", channel["caller_id_number"])
else
  if dbh:connected() == true then
    log("DBH Connected : releasing","","debug")
    assert(dbh:release())
  end
end

-----------------------------------------------
--        Get Customer Rate
-----------------------------------------------
if (session:ready() == true) then
  rate = {}
  local rateprio = 1
  rateok = 0
  while rateok == 0 do
    log("rateprio / rateok :", rateprio.." / "..rateok)
    if rateprio == 8 then
      break
    else
        if channel["call-type"] == "DIDIN" then
            query_rate_sql = [[SELECT
                rc.lcrgroup_id AS lcrgroup_id,
                rc.callerid_filter AS callerid_filter,
                rc.rctype AS rctype,
                rc.id AS ratecard_id,
                r.destination AS destination,
                r.prefix AS prefix,
                r.rate AS rate,
                r.block_min_duration AS block_min_duration,
                r.init_block AS init_block,
                r.minimal_time AS minimal_time,
                0 AS discount
                FROM ratecard rc
                INNER JOIN customer_rates r
                  ON rc.id = r.ratecard_id ]] .. ratecardfilter .. [[
                WHERE rc.enabled = TRUE
                  AND rc.id = ']] .. customer["cust_ratecard"] .. [['
                  AND r.enabled = true
                  AND now() > rc.date_start
                  AND now() < rc.date_end
                  AND ']] .. channel["destination_number"] .. [[' LIKE concat(r.prefix,'%')
                ORDER BY LENGTH(r.prefix) desc LIMIT 1]]
            rateprio = 7
        else
          query_rate_sql = [[SELECT * FROM ( SELECT
              CASE
                WHEN (r.destnum_length - LENGTH(']] .. channel["destination_number"] .. [[') = 0) THEN 0
                WHEN ((r.destnum_length - LENGTH(']] .. channel["destination_number"] .. [[')) <> 0 AND r.destnum_length = 0) THEN 1
                ELSE 2
              END AS destnum_length_map,
              r.destnum_length,
              c.tech_prefix AS tech_prefix,
              c.ratecard_id AS ratecard_id,
              c.priority AS priority,
              c.discount AS discount,
              c.allow_negative_margin AS allow_negative_margin,
              rc.lcrgroup_id AS lcrgroup_id,
              rc.callerid_filter AS callerid_filter,
              rc.rctype AS rctype,
              r.destination AS destination,
              r.prefix AS prefix,
              r.rate AS rate,
              r.block_min_duration AS block_min_duration,
              r.init_block AS init_block,
              r.minimal_time AS minimal_time,
              lg.name AS lcrgoup,
              lg.lcrtype AS lcrtype,
              cip.prefix AS cip_prefix
              FROM customer_ratecards c
              INNER JOIN ratecard rc
                ON rc.id = c.ratecard_id
                  AND c.company_id = ']] .. channel["accountcode"] .. [['
                  AND c.priority = ']] .. rateprio .. [['
                  AND now() > rc.date_start
                  AND now() < rc.date_end
              INNER JOIN lcr_group lg
                ON lg.id = rc.lcrgroup_id
              LEFT JOIN caller_id_prefix cip
                ON cip.calleridprefixlist_id = rc.callerid_list_id
                  AND ']] .. pyfb_caller_id_number .. [[' LIKE concat(cip.prefix,'%')
              INNER JOIN customer_rates r
                ON rc.id = r.ratecard_id ]] .. ratecardfilter .. [[
              WHERE rc.enabled = TRUE
                AND r.enabled = true
                AND ']] .. channel["destination_number"] .. [[' LIKE concat(c.tech_prefix,r.prefix,'%')
              ) T
              WHERE destnum_length_map <> 2
              ORDER BY destnum_length_map, LENGTH(prefix) desc LIMIT 1]]
        end

      log("SQL: ", query_rate_sql, "debug")
      assert(dbh:query(query_rate_sql, function(row)
        for key, val in pairs(row) do
          rate[key] = val
        end
        -- log("Callerid filter value", rate["callerid_filter"] .. " / " .. rate["cip_prefix"])
        if rate["callerid_filter"] == "1" then
          log("CallerID filter : ", "OFF")
          rateok = 1
        elseif rate["callerid_filter"] == "2" then
          if rate["cip_prefix"] == "" then
            log("CallerID filter : ", "prefix authorized not in list - NOK")
            rateok = 0
          else
            log("CallerID filter : ", "prefix authorized in list - OK")
            rateok = 1
          end
        elseif rate["callerid_filter"] == "3" then
          if rate["cip_prefix"] == "" then
            log("CallerID filter : ", "prefix prohibited not in list - OK")
            rateok = 1
          else
            log("CallerID filter : ", "prefix prohibited in list - NOK")
            rateok = 0
          end
        end
      end))
      rateprio = rateprio + 1
    end
  end
  log("Customer rate - num of records", rateok, "debug")
  log("Customer rate OK: ", rateok)
  if rateok == 0 then
    set_variable("proto_specific_hangup_cause", "PFB_CUSTOMER_RATE_NOT_FOUND")
    log("RATE NOT FOUND! : ", "Exiting")
    session:hangup("BEARERCAPABILITY_NOTAVAIL")
  else
    rate["rate"] = tonumber(rate["rate"])*(1-tonumber(rate["discount"])/100)
    rate["minimal"] = tonumber(rate["minimal_time"]) * tonumber(rate["rate"] / 60) + tonumber(rate["init_block"])
    log("Rate", "OK")
    set_variable("sell_rate", tonumber(rate["rate"]))
    set_variable("sell_increment", rate["block_min_duration"])
    set_variable("prefix", rate["prefix"])
    set_variable("init_block", rate["init_block"])
    set_variable("sell_minimum", tonumber(rate["minimal"]))
    set_variable("ratecard_id", rate["ratecard_id"])
    set_variable("lcr_group_id", rate["lcrgroup_id"])
    set_variable("sell_destination", rate["destination"])
  end
    -- test block prefix with rate -1
  if rate["rate"] == -1 then
    log("Blocked prefix ! : ", "Exiting")
    set_variable("proto_specific_hangup_cause", "PFB_CUSTOMER_PREFIX_BLOCKED")
    session:hangup("BEARERCAPABILITY_NOTAVAIL")
  else
    log("non blocked prefix : ", "OK!", "debug")
  end

  -- Destination Number - remove tech prefix
  if (rate["tech_prefix"] == "" or rate["tech_prefix"] == nil) then
    log("No tech prefix : "," continue","debug")
  else
    log("tech prefix : "," remove it","debug")
    channel["destination_number"] = string.gsub(channel["destination_number"], rate["tech_prefix"], "", 1)
    set_variable("destination_number", channel["destination_number"])
  end

else
  if dbh:connected() == true then
    log("DBH Connected : releasing","","debug")
    assert(dbh:release())
  end
end

-----------------------------------------------
--        EMERGENCY CALLS
-----------------------------------------------
if channel["call-type"] == "EMERGENCY" then
    -- Get corresponding INSEE code
    inseecode = {}
    inseecode_sql1 = [[SELECT
        insee_code
        FROM did d
        WHERE d.number=']] .. pyfb_caller_id_number .. [[']]
    log("SQL: ", inseecode_sql1, "debug")
    assert(dbh:query(inseecode_sql1, function(row)
      for key, val in pairs(row) do
        inseecode[key] = val
      end
    end))

    if inseecode["insee_code"] == '' or inseecode["insee_code"] == nil then
        inseecode_sql2 = [[SELECT
            insee_code
            FROM customer_directory cd
            WHERE cd.name=']] .. channel["sipaccountcode"] .. [[']]

        log("SQL: ", inseecode_sql2, "debug")
        assert(dbh:query(inseecode_sql2, function(row)
          for key, val in pairs(row) do
            inseecode[key] = val
          end
        end))
    end

    if inseecode["insee_code"] == '' or inseecode["insee_code"] == nil then
      -- no inseecode found
      set_variable("proto_specific_hangup_cause", "PFB_EMERGENCY_INSEECODE_NOT_FOUND")
      log("EMERGENCY CALL - INSEE CODE NOT FOUND! : ", "Exiting")
      session:hangup("BEARERCAPABILITY_NOTAVAIL")
    else
      log("EMERGENCY CALL - INSEE CODE FOUND! : ", inseecode["insee_code"])
    end
    -- Get corresponding long number
    urgency = {}
    urgency_number_sql = [[SELECT
        ui.insee_code,
        uc.long_number,
        uu.number
        FROM "urgencyfr-inseecitycode" ui
        INNER JOIN "urgencyfr-pdau" up
            ON up.insee_code_id = ui.id AND up.enabled=TRUE
        INNER JOIN "urgencyfr-caau" uc
            ON caau_id = uc.id AND uc.enabled=True
        INNER JOIN "urgencyfr-urgencynumber" uu
            ON up.urgencynumber_id = uu.id
              AND uu.number=']] .. channel["destination_number"] .. [['
        WHERE ui.insee_code=']] .. inseecode["insee_code"] .. [[']]

    log("SQL: ", urgency_number_sql, "debug")
    assert(dbh:query(urgency_number_sql, function(row)
      for key, val in pairs(row) do
        urgency[key] = val
      end
    end))
    if urgency["long_number"] == '' or urgency["long_number"] == nil then
        -- no inssecode found
        set_variable("proto_specific_hangup_cause", "PFB_EMERGENCY_LONG_NUMBER_NOT_FOUND")
        log("REMERGENCY CALL - LONG NUMBER NOT FOUND! : ", "Exiting")
        session:hangup("BEARERCAPABILITY_NOTAVAIL")
    else
        -- remove +
        urgency["long_number"] = string.gsub(urgency["long_number"], "+", "", 1)
        channel["destination_number"] = urgency["long_number"]
    end
end

-----------------------------------------------
--        SELECT LCR TYPE
-----------------------------------------------
if (session:ready() == true) then
  log("LCR Type : ", rate["lcrtype"])
  if rate["lcrtype"] == "p" then
    ratefilter = "cost_rate ASC, random()"
    log("LCR Type : ", "Price")
  elseif rate["lcrtype"] == "q" then
    ratefilter = "quality DESC, random()"
    log("LCR Type : ", "Quality")
  elseif rate["lcrtype"] == "r" then
    ratefilter = "reliability DESC, random()"
    log("LCR Type : ", "Reliability")
  elseif rate["lcrtype"] == "l" then
    ratefilter = "random()"
    log("LCR Type : ", "LoadBalancing")
  end
-----------------------------------------------
--        Get LCR / Gateway
-----------------------------------------------
   -- route only on cost rate - other routing purpose to be implemented
  lcrok = 1
  lcr = {}
  lcr_channels = {}
  lcr_gwprefix = {}
  lcr_gwsuffix = {}
  lcr_codec = {}
  lcr_gwname = {}
  lcr_gwusername = {}
  lcr_gwpassword = {}
  lcr_gwregister = {}
  lcr_gwproxy = {}
  lcr_gwrealm = {}
  lcr_gwfrom_domain = {}
  lcr_gwexprire_seconds = {}
  lcr_gwretry_seconds = {}
  lcr_gwcaller_id_in_from = {}
  lcr_sipcidtype = {}
  lcr_lcrname = {}
  lcr_lcrtype = {}
  lcr_digits = {}
  lcr_destination = {}
  lcr_cost_rate = {}
  lcr_block_min_duration = {}
  lcr_init_block = {}
  lcr_carrier = {}
  lcr_lead_strip = {}
  lcr_tail_strip = {}
  lcr_prefix = {}
  lcr_suffix = {}
  lcr_quality = {}
  lcr_reliability = {}
  lcr_gwid = {}
  lcr_remove_prefix = {}
  lcr_add_prefix = {}
  if channel["call-type"] == "DIDIN" then
      query_cost_sql = [[SELECT
              pr.destination AS destination,
              pr.digits AS digits,
              pr.cost_rate AS cost_rate,
              pr.block_min_duration AS block_min_duration,
              pr.init_block AS init_block,
              pt.carrier_id AS carrier_id
              FROM provider_tariff pt
              INNER JOIN provider_rates pr
                ON pr.provider_tariff_id = pt.id
                  AND pr.enabled = TRUE
                  AND ']] .. channel["destination_number"] .. [[' LIKE concat(pr.digits,'%')
              WHERE pt.id = ']] .. customer["prov_ratecard"] .. [['
                AND pt.enabled = TRUE
                AND now() > pt.date_start
                AND now() < pt.date_end
              ORDER BY LENGTH(pr.digits) DESC]]

      assert(dbh:query(query_cost_sql, function(row)
        lcr_digits[lcrok] = tonumber(row.digits)
        lcr_destination[lcrok] = row.destination
        lcr_cost_rate[lcrok] = tonumber(row.cost_rate)
        lcr_block_min_duration[lcrok] = tonumber(row.block_min_duration)
        lcr_init_block[lcrok] = tonumber(row.init_block)
        lcrok = lcrok + 1
      end))
  else
      if rate["allow_negative_margin"] == "1" then
        log("Negative margin allowed","","info")
        negativemargin = " "
      else
        log("Negative margin forbidden","","info")
        negativemargin = " WHERE T.cost_rate <= "..tonumber(rate["rate"]).." "
      end
      log("rate_lcrgroup_id : ", rate["lcrgroup_id"], "debug")
      query_cost_sql = [[SELECT
          T.destination AS destination,
          T.digits AS digits,
          T.cost_rate AS cost_rate,
          T.block_min_duration AS block_min_duration,
          T.init_block AS init_block,
          T.carrier_id AS carrier_id,
          T.lead_strip AS lead_strip,
          T.tail_strip AS tail_strip,
          T.prefix AS prefix,
          T.suffix AS suffix,
          T.quality AS quality,
          T.reliability AS reliability,
          s.sip_cid_type AS sip_cid_type,
          s.channels AS channels,
          s.prefix AS gwprefix,
          s.suffix AS gwsuffix,
          s.codec AS codec,
          s.name AS gwname,
          s.id AS gwid,
          s.username AS gwusername,
          s.password AS gwpassword,
          s.register AS gwregister,
          s.proxy AS gwproxy,
          s.realm AS gwrealm,
          s.from_domain AS gwfrom_domain,
          s.expire_seconds AS gwexprire_seconds,
          s.retry_seconds AS gwretry_seconds,
          s.caller_id_in_from AS gwcaller_id_in_from,
          ccnr.remove_prefix,
          ccnr.add_prefix
          FROM
            (SELECT DISTINCT ON (pr.provider_tariff_id)
              pr.destination AS destination,
              pr.digits AS digits,
              pr.cost_rate AS cost_rate,
              pr.block_min_duration AS block_min_duration,
              pr.init_block AS init_block,
              pt.carrier_id AS carrier_id,
              pt.lead_strip AS lead_strip,
              pt.tail_strip AS tail_strip,
              pt.prefix AS prefix,
              pt.suffix AS suffix,
              pt.quality AS quality,
              pt.reliability AS reliability
              FROM lcr_providers lp
              INNER JOIN provider_tariff pt
                ON pt.id = lp.provider_tariff_id
                  AND pt.enabled = TRUE
                  AND now() > pt.date_start
                  AND now() < pt.date_end
              INNER JOIN provider_rates pr
                ON pr.provider_tariff_id = pt.id
                  AND pr.enabled = TRUE
                  AND ']] .. channel["destination_number"] .. [[' LIKE concat(pr.digits,'%')
              WHERE lp.lcr_id = ']] .. rate["lcrgroup_id"] .. [['
              ORDER BY pr.provider_tariff_id, LENGTH(pr.digits) DESC
            ) T
          INNER JOIN sofia_gateway s
            ON s.company_id = T.carrier_id
              AND s.enabled = TRUE
          LEFT JOIN carrier_cid_norm_rules ccnr
            ON ccnr.company_id = T.carrier_id
              AND ']] .. pyfb_caller_id_number .. [[' LIKE concat(ccnr.prefix, '%') ]]
          .. negativemargin .. [[ORDER BY ]] .. ratefilter

      assert(dbh:query(query_cost_sql, function(row)
        lcr_channels[lcrok] = tonumber(row.channels)
        lcr_gwprefix[lcrok] = row.gwprefix
        lcr_gwsuffix[lcrok] = row.gwsuffix
        lcr_codec[lcrok] = row.codec
        lcr_gwproxy[lcrok] = row.gwproxy
        lcr_gwrealm[lcrok] = row.gwrealm
        lcr_gwfrom_domain[lcrok] = row.gwfrom_domain
        lcr_gwexprire_seconds[lcrok] = row.gwexprire_seconds
        lcr_gwretry_seconds[lcrok] = row.gwretry_seconds
        lcr_gwcaller_id_in_from[lcrok] = row.gwcaller_id_in_from
        lcr_sipcidtype[lcrok] = row.sip_cid_type
        lcr_lcrname[lcrok] = rate["lcrgroup"]
        lcr_lcrtype[lcrok] = rate["lcrtype"]
        lcr_digits[lcrok] = tonumber(row.digits)
        lcr_destination[lcrok] = row.destination
        lcr_cost_rate[lcrok] = tonumber(row.cost_rate)
        lcr_block_min_duration[lcrok] = tonumber(row.block_min_duration)
        lcr_init_block[lcrok] = tonumber(row.init_block)
        lcr_carrier[lcrok] = row.carrier_id
        lcr_lead_strip[lcrok] = row.lead_strip
        lcr_tail_strip[lcrok] = row.tail_strip
        lcr_prefix[lcrok] = row.prefix
        lcr_suffix[lcrok] = row.suffix
        lcr_quality[lcrok] = row.quality
        lcr_reliability[lcrok] = row.reliability
        lcr_gwid[lcrok] = row.gwid
        lcr_remove_prefix[lcrok] = row.remove_prefix
        lcr_add_prefix[lcrok] = row.add_prefix
        lcrok = lcrok + 1
      end))
  end
  log("SQL: ", query_cost_sql, "debug")
  lcrok = lcrok - 1
  log("lcr - num of records", lcrok, "debug")
  if lcrok == 0 then
    set_variable("proto_specific_hangup_cause", "PFB_PROVIDER_RATE_NOT_FOUND")
    session:hangup("BEARERCAPABILITY_NOTAVAIL")
  else
    log("lcr", "OK")
  end
else
  if dbh:connected() == true then
    log("DBH Connected : releasing","","debug")
    assert(dbh:release())
  end
end
if (session:ready() == true) then
-----------------------------------------------
--        BRIDGING
-----------------------------------------------
--  set_variable("effective_caller_id_number", channel["caller_id_number"])
  set_variable("effective_caller_id_name", channel["caller_id_name"])
  set_variable("effective_callee_id_number", channel["destination_number"])
  set_variable("effective_callee_id_name", "_undef_")

  set_variable("bypass_media", "false")
  set_variable("hangup_after_bridge", "true")
  execute("set", "continue_on_fail=1,2,3,6,25,34,38,41,42,44,47,63,66,403,480,488,500,501,502,503")
--  execute("set", "continue_on_fail=true")
  execute("set", "bypass_media=false")
  execute("sched_hangup", "+36000 alloted_timeout")
  execute("set", "inherit_codec=true")
  execute("set", "disable_hold=true")
  if channel["fake_ring"] == "True" then
    execute("set", "ringback=%(2000,4000,440.0,480.0)")
    execute("set", "instant_ringback=true")
  end

-----------------------------------------------
-- VoiceMail Detection variables
-----------------------------------------------
  if channel["vmd"] == "True" then
    human_detected = false
    voicemail_detected = false
    session:setInputCallback("onInput")
    execute("set", "api_result=${sched_api(+5 none avmd "..channel["uuid"].." start)}")
  end

--    execute("export", "disable_q850_reason=true")
--    execute("nibblebill", "check")
  mydialbridge = ""
  myvarbridge = ""

-- currency start : if no rate setup error message - for that add special variable - and prevent executing failed bridge - new special message : PFB_PROVIDER_RATE_FOUND_BUT_NEGATIVE_MARGIN - if negative margin allow bridge, but alert message !!!
-- start for boucle
  for i=1,lcrok do
--    if (session:ready() == true) then
      if channel["call-type"] == "PSTN" or channel["call-type"] == "EMERGENCY" then
          if lcr_lead_strip[i] == "" then
            lcr_lead_strip[i]  = "^"
          end
          log("WS CALL strip:", lcr_lead_strip[i])
          log("WS CALL prefix:", lcr_prefix[i])
          log("WS CALL dest number:", channel["destination_number"])
          log("WS CALL gwprefix :", lcr_gwprefix[i])
          called_number = string.gsub(channel["destination_number"], lcr_lead_strip[i], lcr_gwprefix[i]..lcr_prefix[i], 1)
          log("WS CALL CallerID strip prefix:", lcr_remove_prefix[i])
          log("WS CALL CallerID number:", channel["caller_id_number"])
          log("WS CALL CallerID add prefix :", lcr_add_prefix[i])
          -- test if the callerID start with a + and the gw prefix is a + to avoid ++
          if lcr_add_prefix[i] == "+" then
              channel["caller_id_number"] = string.gsub(channel["caller_id_number"], "+", "", 1)
          end
          caller_id = string.gsub(channel["caller_id_number"], lcr_remove_prefix[i], lcr_add_prefix[i], 1)
          log("WS CALL CallerID sent to provider: ", caller_id)
          log("WS CALL dest num with prefix/suffix/strip : ", called_number)
      else
          called_number = channel["destination_number"]
          caller_id = channel["caller_id_number"]
      end

      myvarbridge = "nobal_amt="..tonumber(customer["credit_limit"])
      if channel["call-type"] == "PSTN" or channel["call-type"] == "EMERGENCY" then
          -- myvarbridge = myvarbridge .. ",execute_on_post_originate=limit hash outbound "..lcr_gwname[i].." "..lcr_channels[i].." !NORMAL_TEMPORARY_FAILURE"
      end
      -- myvarbridge = myvarbridge .. ",sip_from_uri=sip:"..caller_id.."@"..channel["kam_received_ip"]
      myvarbridge = myvarbridge .. ",origination_caller_id_number="..caller_id
      myvarbridge = myvarbridge .. ",origination_caller_id_name="..caller_id
      myvarbridge = myvarbridge .. ",sell_destination="..rate["destination"]
      myvarbridge = myvarbridge .. ",prefix="..rate["prefix"]
      myvarbridge = myvarbridge .. ",sell_rate="..tonumber(rate["rate"])
      myvarbridge = myvarbridge .. ",sell_increment="..rate["block_min_duration"]
      myvarbridge = myvarbridge .. ",destination_number="..channel["destination_number"]
      myvarbridge = myvarbridge .. ",user_agent="..channel["sip_user_agent"]
      myvarbridge = myvarbridge .. ",customer_ip="..channel["sip_received_ip"]
      myvarbridge = myvarbridge .. ",nibble_rate="..tonumber(rate["rate"])
      myvarbridge = myvarbridge .. ",nibble_minimum="..tonumber(rate["minimal"])
      myvarbridge = myvarbridge .. ",nibble_account="..channel["accountcode"]
      if channel["call-type"] == "DIDIN" then
          execute("set", "sip_h_X-PyFB-SIPAccountId=" .. customer["sipname"])
      elseif channel["call-type"] == "DIDOUT" then
          -- get sipaccont of destnum
          dnsipcode = {}
          dnsipcode_sql = [[SELECT
              d.id,
              dr.trunk_id,
              cd.name
              FROM did d
              INNER JOIN did_routes dr
                ON dr.contract_did_id = d.id
              INNER JOIN customer_directory cd
                ON cd.id = dr.trunk_id
              WHERE d.number=']] .. channel["destination_number"] .. [[']]
          log("SQL: ", dnsipcode_sql, "debug")
          assert(dbh:query(dnsipcode_sql, function(row)
            for key, val in pairs(row) do
              dnsipcode[key] = val
            end
          end))
          if dnsipcode["name"] == '' or dnsipcode["name"] == 'nil' then
              log("No coresponding destnum sip account found for didout")
          else
              execute("set", "sip_h_X-PyFB-SIPAccountId=" .. dnsipcode["name"])
          end
      end
      myvarbridge = myvarbridge .. ",nibble_increment="..rate["block_min_duration"]
      myvarbridge = myvarbridge .. ",init_block="..tonumber(rate["init_block"])
      myvarbridge = myvarbridge .. ",customer="..channel["accountcode"]
      if channel["call-type"] == "PSTN" or channel["call-type"] == "EMERGENCY" then
          myvarbridge = myvarbridge .. ",gateway="..lcr_gwid[i]
          myvarbridge = myvarbridge .. ",sip_cid_type="..lcr_sipcidtype[i]
      end
      if channel["call-type"] == "PSTN" or channel["call-type"] == "DIDIN" or channel["call-type"] == "EMERGENCY" then
          myvarbridge = myvarbridge .. ",cost_rate="..lcr_cost_rate[i]
          myvarbridge = myvarbridge .. ",cost_destination="..lcr_destination[i]
      elseif channel["call-type"] == "DIDOUT" then
          myvarbridge = myvarbridge .. ",cost_rate=0"
          myvarbridge = myvarbridge .. ",cost_destination=DIDOUT"
      end
      if channel["call-type"] == "PSTN" or channel["call-type"] == "EMERGENCY" then
          myvarbridge = myvarbridge .. ",lcr_carrier_id="..lcr_carrier[i]
          myvarbridge = myvarbridge .. ",lcr_group_id="..rate["lcrgroup_id"]
      end
      myvarbridge = myvarbridge .. ",ratecard_id="..rate["ratecard_id"]
      if channel["call-type"] == "PSTN" or channel["call-type"] == "EMERGENCY" then
          myvarbridge = myvarbridge .. ",caller-id-in-from="..lcr_gwcaller_id_in_from[i]
          -- ToDo myvarbridge = myvarbridge .. ",username="..lcr_gwusername[i]
          myvarbridge = myvarbridge .. ",expire_seconds="..lcr_gwexprire_seconds[i]
          myvarbridge = myvarbridge .. ",retry_seconds="..lcr_gwretry_seconds[i]
          if lcr_gwfrom_domain then
            myvarbridge = myvarbridge .. ",sip_invite_domain="..lcr_gwfrom_domain[i]
            myvarbridge = myvarbridge .. ",from-domain="..lcr_gwfrom_domain[i]
          end
          -- ToDo myvarbridge = myvarbridge .. ",realm="..lcr_gwrealm[i]
      end

      log("WS CALL my variables bridge : ", myvarbridge)
      if mydialbridge == "" then
          mydialbridge = "{ignore_early_media=" .. channel["ignore_early_media"] .. "}[" .. myvarbridge .. "]sofia/"..myprofile.."/" .. called_number
          if channel["call-type"] == "PSTN" or channel["call-type"] == "EMERGENCY" then
              mydialbridge = mydialbridge  .. "@" .. lcr_gwproxy[i]
          else
              mydialbridge = mydialbridge  .. "@" .. channel["internal_kam_ip"] .. ":5060"
              -- end boucle
              i=lcrok
          end

      else
        mydialbridge = mydialbridge .. "|[" .. myvarbridge .. "]sofia/"..myprofile.."/" .. called_number .. "@" .. lcr_gwproxy[i]
      end
      log("construction bridge : ", mydialbridge, "debug")
-- set call limit
      --execute("limit_execute", "hash outbound "..lcr_gwname[i].." "..lcr_channels[lcrok].." bridge "..mydialbridge)
--    end
  end
-- end for boucle

  log("BRIDGE EXECUTE:", mydialbridge, "debug")
  -- execute("bridge", mydialbridge)
  --session:hangup()
  assert(dbh:release())
  session:execute("set", "pyfb_bridge="..mydialbridge)
end
if dbh:connected() == true then
  log("DBH Connected : releasing","","debug")
  assert(dbh:release())
end
freeswitch.consoleLog("info", "WS CALL -> Bridging... <-----------\n");
