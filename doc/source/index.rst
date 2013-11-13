.. PyFreeBilling, Wholesale billing and softswitch application based on Freeswitch documentation master file, created by
   sphinx-quickstart on Wed Nov 13 11:05:35 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyFreeBilling's documentation!
=========================================
**Wholesale billing and softswitch application based on Freeswitch**

--------------

::

                             Table of content

--------------

-  About pyfreebilling
-  License
-  Features
-  Prerequisites
-  Installation
-  Contact information

--------------

::

                             What is pyfreebilling

--------------

pyfreebilling is an open source wholesale billing platform for
FreeSWITCH.

pyfreebilling is developed under python, LUA and PostgreSQL as the
database layer.

--------------

::

                             License

--------------

pyfreebilling is under GPLv3 license. You can read it in COPYING file.

--------------

::

                             Features

--------------

There are a some features supported. Most of them are configurable via
the web interface. A few of them are:

-  Customer add/modify/delete
-  IP termination
-  SIP authentication
-  Prepaid and/or postpaid
-  Realtime billing
-  Block calls on negative balance (prepaid) or balance under credit
   limit (postpaid)
-  Block / allow negative margin calls
-  Email alerts
-  Daily balance email to customer
-  Limit the maximum number of calls per customer and/or per gateway
-  Multiple contexts
-  Tons of media handling options
-  Powerfull ratecard engine

-  Provider add/modify/delete
-  Powerful LCR engine
-  Routing based on area code
-  Routing decision based on quality, reliability, cost or load
   balancing (equal)
-  Limit max channels by each provider gateway

-  Extensive call and financial reporting screens (TBD)

-  CDR export to CSV

-  Design for scalability

... and much more :)

--------------

::

                             Prerequisites

--------------

In order to run pyfreebilling, you need the following configured,
secured and working Basic Operating System (Linux or BSD, but also
windows).

The project uses freeswitch, PostgreSQL and Django.

--------------

::

                             Contact Information

--------------

Name: Mathias WOLFF Email: website contact form Website:
http://www.blog-des-telecoms.com // specific parts will be created

--------------

::

                             Contents

--------------

.. toctree::
   :maxdepth: 2
   
   license
   installation



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

