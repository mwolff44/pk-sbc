--# Copyright 2017 Mathias WOLFF
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
--        IMPORT CDR SCRIPT
-----------------------------------------------

-- Pre-requesites : lua5.2 : apt-get install lua5.2 lua-sql-postgres

-----------------------------------------------
-- CDR CSV File format :
--[[
1- customer_id, customer_ip,
3- uuid,
4- caller_id_number, destination_number,
6- chan_name,
7- start_stamp, answered_stamp, end_stamp, duration,
11- read_codec, write_codec, 
13- hangup_cause, hangup_cause_q850, 
15- gateway_id, 
16- cost_rate, prefix, "", rate, init_block, block_min_duration, 
22- lcr_carrier_id_id, ratecard_id_id, lcr_group_id_id, 
25- sip_user_agent, 
26- sip_rtp_rxstat, sip_rtp_txstat, 
28- bleg_uuid, 
29- switchname, switch_ipv4, 
31- hangup_disposition, billmsec, sip_hangup_cause,  
34- sell_destination, cost_destination
]]
-----------------------------------------------
-----------------------------------------------
--        FUNCTIONS
-----------------------------------------------
-----------------------------------------------

-----------------------------------------------
--        ROUND
-----------------------------------------------
function round(num, dec)
    if num == 0 then
        return 0
    else
        local mult = 10^(dec or 0)
        return math.floor(num * mult + 0.5) / mult
    end
end

-----------------------------------------------
--        CSV READ
-----------------------------------------------
--[[
-------------------------------
ORIGINAL SOURCE CODE : http://nocurve.com/2014/03/05/simple-csv-read-and-write-using-lua/
Modified by Mathias WOLFF
-------------------------------

Example use: Suppose file csv1.txt is:

1.23,70,hello
there,9.81,102
x,y,,z
8,1.243,test

Then the following
-------------------------------------
local csvfile = require "simplecsv"
local m = csvfile.read('./csv1.txt') -- read file csv1.txt to matrix m
print(m[2][3])                       -- display element in row 2 column 3 (102)
m[1][3] = 'changed'                  -- change element in row 1 column 3
m[2][3] = 123.45                     -- change element in row 2 column 3
-------------------------------------

the read method takes 4 parameters:
path: the path of the CSV file to read - mandatory
sep: the separator character of the fields. Optionsl, defaults to ','
tonum: whether to convert fields to numbers if possible. Optional. Defaults to true
null: what value should null fields get. Optional. defaults to ''
]]
---------------------------------------------------------------------
function string:split(sSeparator, nMax, bRegexp)
    if sSeparator == '' then
        sSeparator = ','
    end

    if nMax and nMax < 1 then
        nMax = nil
    end

    local aRecord = {}

    if self:len() > 0 then
        local bPlain = not bRegexp
        nMax = nMax or -1

        local nField, nStart = 1, 1
        local nFirst,nLast = self:find(sSeparator, nStart, bPlain)
        while nFirst and nMax ~= 0 do
            aRecord[nField] = self:sub(nStart, nFirst-1)
            nField = nField+1
            nStart = nLast+1
            nFirst,nLast = self:find(sSeparator, nStart, bPlain)
            nMax = nMax-1
        end
        aRecord[nField] = self:sub(nStart)
    end

    return aRecord
end

---------------------------------------------------------------------
function read(path, sep, tonum, null)
    tonum = tonum or true
    sep = sep or ','
    null = null or ''
    local csvFile = {}  -- table to collect fields
    local file = assert(io.open(path, "r"))
    local effectiveduration = 0
    local billsec = 0
    local totalsell = 0
    local totalcost = 0
    for line in file:lines() do
        fields = line:split(sep)
        if tonum then -- convert numeric fields to numbers - strip " and '
            for i=1,#fields do
                local field = fields[i]:gsub('"', ''):gsub('\'', '')
                if field == '' then
                    field = null
                end
                if i == 29 then
                    fields[i] = fsname
                elseif i == 30 then
                    fields[i] = fsipaddr
                else
                    fields[i] = tonumber(field) or field
                end
            end
        end

        -- effectiveduration
        if fields[32] == nil then
            effectiveduration = tonumber(0)
        else
            effectiveduration = math.ceil(tonumber(fields[32] / 1000))
        end
        fields[36] = effectiveduration + 16
        -- billed duration
        if (effectiveduration ~= 0  and fields[21] == not nil) then
            if effectiveduration < fields[21] then
                billsec = tonumber(fields[21])
            else
                billsec = math.ceil(effectiveduration / fields[21]) * fields[21]
            end
        else
            billsec = effectiveduration
        end
        fields[37] = billsec
        -- total sell
        if (fields[19] == not nil and fields[19] ~= 0) then
            totalsell = round((billsec * fields[19] / 60), 6)
        else
            totalsell = tonumber(0)
        end
        if (fields[20] == not nil and billsec ~=0) then
            totalsell = round((totalsell + fields[20]), 6)
        end
        fields[38] = totalsell
        -- total cost
        if (fields[19] == not nil) then
            totalcost = round((billsec * fields[16] / 60), 6)
        else
            totalcost = tonumber(0)
        end
        --table.insert(fields, totalcost)
        fields[39] = totalcost

        table.insert(csvFile, fields)
        
    end
    file:close()
    return csvFile
end

-----------------------------------------------
--        CDR CSV FILE ROTATE
-----------------------------------------------
function cdrcsvfilerotate()
    local status,reason,infonum=os.execute("fs_cli -x 'cdr_csv rotate'")
    if status then
        print("importcdr : ", "cdr csv file rotation done : " .. infonum)
    else
        print("importcdr : ", "cdr csv file rotation error : " .. reason)
    end
end

-----------------------------------------------
-----------------------------------------------
--        SCRIPT START
-----------------------------------------------
-----------------------------------------------

-- Settings
csvbasedir = '/tmp/cdr-csv/'
csvbasename = 'Master.csv.'
fsname = "jessie1"
fsipaddr = ""

print("hello")

-- DB connexion
-- load driver
local driver = require "luasql.postgres"
-- create environment object
env = assert (driver.postgres())
-- connect to data source
con = assert (env:connect("pyfreebilling", "pyfreebilling", "password", "localhost", "5432"))

-- cdr csv file rotate

-- load csv files to table
local m = read(csvbasedir .. csvbasename .. "1", ',', true, "NULL")
print(table.unpack(m[1]))
--for key,value in ipairs(m) do #table.unpack[value] end
print("Nb CDR to be imported : " .. #m)

-- clean table
--- delete row with no fields if #m[i] == 0 then remove m[i]

-- load to cdr DB
-- a ameliorer - fonctionnel mais pas elegant
for index, p in ipairs(m) do
  re = assert(con:execute(string.format([[
    INSERT INTO cdr (id, customer_id, customer_ip, uuid, caller_id_number, destination_number, chan_name, start_stamp, answered_stamp, end_stamp, duration, read_codec, write_codec, hangup_cause, hangup_cause_q850, gateway_id, cost_rate, prefix, country, rate, init_block, block_min_duration, lcr_carrier_id_id, ratecard_id_id, lcr_group_id_id, sip_user_agent, sip_rtp_rxstat, sip_rtp_txstat, bleg_uuid, switchname, switch_ipv4, hangup_disposition, effectiv_duration, sip_hangup_cause, sell_destination, cost_destination, effective_duration, billsec, total_sell, total_cost)
    VALUES (DEFAULT, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')]], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12], p[13], p[14], p[15], p[16], p[17], p[18], p[19], p[20], p[21], p[22], p[23], p[24], p[25], p[26], p[27], p[28], p[29], p[30], p[31], p[32], p[33], p[34], p[35], p[36], p[37], p[38], p[39])
  ))
end

-- calculate stats

-- update supplier balance in DB

-- update stats in DB

-- release DB
-- close everything
--cur:close() -- already closed because all the result set was consumed
con:close()
env:close()
