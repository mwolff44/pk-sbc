
![logo](http://www.pyfreebilling.com/wp-content/uploads/2014/12/PyFreeBilling-logo-small.png)

### Table of content

- About pyfreebilling
- License
- Features
- Prerequisites
- Installation
- Contact information

### What is pyfreebilling

*pyfreebilling* is an *open source wholesale billing platform* for *FreeSWITCH* . 

pyfreebilling is developed under python, LUA and PostgreSQL as the database layer.

### Documentation


Please visit : [http://pyfreebilling.readthedocs.org/](http://pyfreebilling.readthedocs.org/)

### License


pyfreebilling is under GPLv3 license. You can read it in COPYING file.

[![GPLv3 License](http://img.shields.io/badge/license-GPLv3-blue.svg?style=flat-square)](http://www.fsf.org)

### Features

There are a some features supported. Most of them are configurable via the web
interface. A few of them are:

- Customer add/modify/delete
   - IP termination
   - SIP authentication
   - Prepaid and/or postpaid
   - Realtime billing
   - Block calls on negative balance (prepaid) or balance under credit limit (postpaid)
   - Block / allow negative margin calls
   - Email alerts
   - Daily balance email to customer
   - Limit the maximum number of calls per customer and/or per gateway
   - Multiple contexts
   - Tons of media handling options
   - Powerfull ratecard engine

- Provider add/modify/delete
   - Powerful LCR engine
   - Routing based on area code
   - CLI Routing
   - Routing decision based on quality, reliability, cost or load balancing (equal)
   - Limit max channels by each provider gateway

- Extensive call and financial reporting screens (TBD)

- CDR export to CSV

- Customer panel

- Design for scalability

... and much more :)

### Prerequisites

In order to run pyfreebilling, you need the following configured, secured  and 
working Basic Operating System (Linux or BSD, but also windows).

The project uses freeswitch, PostgreSQL and Django.

### Contact Information

Name: _Mathias WOLFF_

Email: _website contact form_


Website: [http://www.pyfreebilling.com](http://www.pyfreebilling.com)

### Screenshots

![Customer panel](http://www.pyfreebilling.com/wp-content/uploads/2014/12/pfb-th-sanstone-inv.png)
![Admin interface](http://www.pyfreebilling.com/wp-content/uploads/2014/03/pyfreebilling-customer-rates2.png)

And many more ... [PyFreeBilling gallery](http://www.pyfreebilling.com/portfolio/)

### Donation

If you want to support my developments you are welcome to buy me a cup of coffee :)

<a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=SWGM9B2YW5VGA" target="_blank">PayPal donation link</a>


