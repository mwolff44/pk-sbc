********************************************************************************
                             Table of content
********************************************************************************

- About pyfreebilling
- License
- Features
- Prerequisites
- Installation
- Contact information

********************************************************************************
                             What is vBilling
********************************************************************************

pyfreebilling is an open source wholesale billing platform for FreeSWITCH. 

pyfreebilling is developed under python, LUA and PostgreSQL as the database layer.

********************************************************************************
                             License
********************************************************************************

pyfreebilling is under GPLv3 license. You can read it in COPYING file.

********************************************************************************
                             Features
********************************************************************************

There are a some features supported. Most of them are configurable via the web
interface. A few of them are:

- Customer add/modify/delete
   - IP termination
   - SIP authentication
   - Prepaid and/or postpaid
   - Realtime billing
   - Prepaid / postpaid
   - Block calls on negative balance (prepaid) or balance under credit limit (postpaid)
   - Limit the maximum number of calls per customer and/or per gateway
   - Multiple contexts
   - Tons of media handling options
   - Powerfull ratecard engine

- Provider add/modify/delete
   - Powerful LCR engine
   - Costs for provider routes based on area code
   - Limit max channels by each provider

- Extensive call and financial reporting screens (TBD)

- CDR export to PDF, CSV and Excel formats (TBD)

- Design for scalability

... and much more :)

********************************************************************************
                             Prerequisites
********************************************************************************

In order to run pyfreebilling, you need the following configured, secured  and 
working Basic Operating System (Linux or BSD, but also windows).

The project use freeswitch, PostgreSQL and Django.

********************************************************************************
                             Contact Information
********************************************************************************

Name: Mathias WOLFF
Email: website contact form
Website: http://www.blog-des-telecoms.com // specific part has to be created
