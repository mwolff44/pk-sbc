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
--        DID WHOLESALE SCRIPT
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
  if channel["cli_debug"] == "True" then
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
--        SCRIPT START
-----------------------------------------------
-----------------------------------------------
-----------------------------------------------
--        GET CHANNEL VARIABLES
-----------------------------------------------
--session:execute("info", "")
--session:setHangupHook("myHangupHook")
channel = {}
if session:ready() then
  channel["cli_debug"] = "True"
  channel["uuid"] = get_Variable("uuid")
  channel["context"] = get_Variable("context")
  channel["destination_number"] = get_Variable("destination_number")
  channel["caller_id_number"] = get_Variable("caller_id_number")
  channel["caller_id_name"] = get_Variable("caller_id_name")
  channel["direction"] = get_Variable("direction")
  channel["session_id"] = get_Variable("session_id")
  channel["sip_from_user"] = get_Variable("sip_from_user")
  channel["sip_received_ip"] = get_Variable("sip_received_ip")
  channel["sip_network_ip"] = get_Variable("sip_network_ip")
  channel["sip_user_agent"] = get_Variable("sip_user_agent")
  channel["fake_ring"] = get_Variable("fake_ring")
  if channel["sip_user_agent"] then
    log("sip_user_agent :", "is OK", "debug")
  else 
    channel["sip_user_agent"] = "not set"
  end
--  channel["FreeSWITCH-IPv4"] = get_Variable("FreeSWITCH-IPv4")
--  channel["FreeSWITCH-Switchname"] = get_Variable("FreeSWITCH-Switchname")
  log("Get session variable :", "done", "debug")
  set_variable("user_agent", channel["sip_user_agent"])
  set_variable("customer_ip", channel["sip_received_ip"])
  set_variable("cost_rate", "0.000000")
  set_variable("sell_rate", "0.000000")
  set_variable("init_block", "0.000000")
  set_variable("sell_increment", "0")
  set_variable("originating_leg_uuid", channel["uuid"])

end

-----------------------------------------------
--        DATABASE CONNECTION
-----------------------------------------------
if session:ready() then
  dbh = freeswitch.Dbh("odbc://freeswitch")
  if dbh:connected() == false then
    set_variable("proto_specific_hangup_cause", "PFB_DB_ERROR")
    log("Dbh : ", "Database error - Hangup call", "ERROR")
    session:hangup("BEARERCAPABILITY_NOTAVAIL")
    return
  else
    log("Dbh : ", "Database connected")
  end
end
-----------------------------------------------
--        Get DID Settings
-----------------------------------------------
if session:ready() then
  if (channel["caller_id_number"] == nil or channel["caller_id_number"] =="") then
    channel["caller_id_number"] = "anonymous"
  end
  did = {{},{}}
  didok = 1
  local query_did_sql = [[SELECT 
      d.provider_id AS provider, 
      d.customer_id AS customer,
      crd.rate AS customer_rate,
      crd.block_min_duration AS customer_block_min_duration,
      crd.interval_duration AS customer_interval_duration,
      d.cust_plan_id AS customer_plan,
      prd.rate AS provider_rate,
      prd.block_min_duration AS provider_block_min_duration,
      prd.interval_duration AS provider_interval_duration,
      d.prov_plan_id AS provider_plan,
      dr.order AS order,
      dr.type AS type,
      dr.trunk_id AS trunk_id,
      c.name AS customer_name,
      c.prepaid AS customer_prepaid,
      c.credit_limit AS credit_limit,
      c.customer_balance AS customer_balance,
      p.name AS provider_name,
      p.supplier_balance AS provider_balance,
      cd.name AS trunk
      FROM did d  
      INNER JOIN customer_rates_did crd 
        ON crd.id = d.cust_plan_id 
          AND crd.enabled = TRUE 
      INNER JOIN provider_rates_did prd 
        ON prd.id = d.prov_plan_id
          AND prd.enabled = TRUE
      INNER JOIN did_routes dr
        ON dr.contract_did_id = d.id
      INNER JOIN company c
        ON c.id = d.customer_id
          AND c.customer_enabled = TRUE
      INNER JOIN company p
        ON p.id = d.provider_id
          AND p.supplier_enabled = TRUE
      INNER JOIN customer_directory cd
        ON cd.id = dr.trunk_id
      WHERE d.number=']] .. channel["destination_number"] .. [['
        ORDER BY dr.order]]

  log("SQL: ", query_did_sql, "debug")
  assert(dbh:query(query_did_sql, function(row)
    for key, val in pairs(row) do
      did[didok][key] = val
    end
    didok = didok + 1
  end))
  assert(dbh:release())
  didok = didok - 1
  log("Customer data - num of records", didok, "debug")
  if didok == 0 then
    set_variable("proto_specific_hangup_cause", "PFB_DID_NOT_FOUND")
    log("DID NOT FOUND!","Exiting")
    session:hangup("BEARERCAPABILITY_NOTAVAIL")
  end
  log("Prepaid / Balance / Credit limit : ".. did[1]["customer_prepaid"] .." /  ".. tonumber(did[1]["customer_balance"]) .." / " .. tonumber(did[1]["credit_limit"]),"")
else
  if dbh:connected() == true then
    log("DBH Connected : releasing","","debug")
    assert(dbh:release())
  end
end

if (session:ready() == true) then 
  if did[1]["customer_prepaid"] == "0" then
    log("Customer...: postpaid","")
    if tonumber(did[1]["customer_balance"]) < tonumber(did[1]["credit_limit"]) then
      set_variable("proto_specific_hangup_cause", "PFB_CUSTOMER_POSTPAID_CREDIT_LIMIT")
      log("CUSTOMER " .. did[1]["customer_name"] .. " has reach credit limit... rejecting","")
      session:hangup("BEARERCAPABILITY_NOTAVAIL");
    else
      log("Credit limit : ","OK")
    end
  elseif did[1]["customer_prepaid"] == "1" then
    log("Customer...: prepaid","")
    if tonumber(did[1]["customer_balance"]) < 0 then
      set_variable("proto_specific_hangup_cause", "PFB_CUSTOMER_PREPAID_NO_MONEY")
      log("CUSTOMER " .. did[1]["customer_name"] .. " has no money... rejecting","")
      session:hangup("BEARERCAPABILITY_NOTAVAIL")
    else
      log("balance : ","OK")
    end
  end
-----------------------------------------------
--        Get Customer Rate
-----------------------------------------------
  set_variable("customer", did[1]["customer"])
  set_variable("sell_rate", tonumber(did[1]["customer_rate"]))
  set_variable("sell_increment", did[1]["customer_interval_duration"])
  set_variable("prefix", channel["destination_number"])
  set_variable("init_block", did[1]["customer_block_min_duration"])
  set_variable("ratecard_id", did[1]["customer_plan"])
  set_variable("lcr_group_id", 0)
  set_variable("sell_destination", "did")
    -- test block prefix with rate -1
  if did[1]["customer_rate"] == -1 then
    log("Blocked prefix ! : ", "Exiting")
    set_variable("proto_specific_hangup_cause", "PFB_CUSTOMER_PREFIX_BLOCKED")
    session:hangup("BEARERCAPABILITY_NOTAVAIL")
  else
    log("non blocked prefix : ", "OK!", "debug")
  end
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
  execute("sched_hangup", "+3600 alloted_timeout")
  execute("set", "inherit_codec=true")
  execute("set", "disable_hold=true")
  if channel["fake_ring"] == "True" then
    execute("set", "ringback=%(2000,4000,440.0,480.0)")
    execute("set", "instant_ringback=true")
  end

  mydialbridge = ""
  myvarbridge = ""
  
-- start for boucle  
  for i=1,didok do
      myvarbridge = "nobal_amt="..tonumber(did[1]["credit_limit"])..", sell_destination=did,cost_destination=did,sell_rate="..tonumber(did[1]["customer_rate"])..",sell_increment="..did[1]["customer_interval_duration"]..",destination_number="..channel["destination_number"]..",user_agent="..channel["sip_user_agent"]..",customer_ip="..channel["sip_received_ip"]..",nibble_rate="..tonumber(did[1]["customer_rate"])..",nibble_account="..did[1]["customer"]..",nibble_increment="..did[1]["customer_interval_duration"]..",customer="..did[1]["customer"]..",gateway="..did[i]["trunk_id"]..",cost_rate="..tonumber(did[i]["provider_rate"])..",prefix=did,init_block="..did[i]["provider_interval_duration"]..",block_min_duration="..did[i]["provider_block_min_duration"]..",lcr_carrier_id="..did[i]["provider"]..",ratecard_id="..did[1]["customer_plan"]..",lcr_group_id=0"
      log("WS CALL my variables bridge : ", myvarbridge)
      if mydialbridge == "" then
        mydialbridge = "[" .. myvarbridge .. "]sofia/internal/" .. did[i]["trunk"] .. "%$${domain}"
      else
        mydialbridge = mydialbridge.."|[" .. myvarbridge .. "]sofia/internal/" .. did[i]["trunk"]
      end
      log("construction bridge : ", mydialbridge, "debug") 
  end
-- end for boucle
  
  log("BRIDGE EXECUTE:", mydialbridge, "debug")
  execute("bridge", mydialbridge)
  session:hangup()          
end
if dbh:connected() == true then
  log("DBH Connected : releasing","","debug")
  assert(dbh:release())
end
freeswitch.consoleLog("info", "WS CALL -> I am now ending... <-----------\n");