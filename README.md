![logo](http://www.pyfreebilling.com/wp-content/uploads/2014/12/PyFreeBilling-logo-small.png)
-------------

![PyFB release](https://img.shields.io/badge/Release-2.2.2-ff69b4.svg)
[![Documentation Status](https://readthedocs.org/projects/pyfreebilling/badge/?version=latest)](http://pyfreebilling.readthedocs.org/en/latest/?badge=latest)
[![Code Health](https://landscape.io/github/mwolff44/pyfreebilling/master/landscape.svg?style=flat)](https://landscape.io/github/mwolff44/pyfreebilling/master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/mwolff44/pyfreebilling/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/mwolff44/pyfreebilling/?branch=master)
[![AGPLv3 License](https://img.shields.io/badge/license-AGPLv3-blue.svg?style=flat-square)](http://www.fsf.org)
[![Donate to this project using Paypal](https://img.shields.io/badge/paypal-donate-red.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=FANG9JC63Q7DY&lc=FR&item_name=PyFreeBilling&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted&pk_campaign=donation)

---


### Table of content

- About pyfreebilling
- License
- Features
- Prerequisites
- Installation
- Contact information
- Screenshots
- Support
- Donation
- Stats

### What is pyfreebilling

*pyfreebilling* is an *open source wholesale billing platform* based on *Kamailio* and *FreeSwitch* .

pyfreebilling is developed under python, LUA and PostgreSQL as the database layer.

### Documentation


Please visit : https://pyfreebilling.readthedocs.org/

### License


pyfreebilling is under AGPLv3 license. You can read it in COPYING file.

[![AGPLv3 License](https://img.shields.io/badge/license-AGPLv3-blue.svg?style=flat-square)](http://www.fsf.org)

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

### Support

To get free support, a dedicated forum is online : [PyFreeBilling community support](https://www.pyfreebilling.org/forum/index.php)

If you need paid support, specific features or consulting services, you will find support services prices on PyFreeBilling website : [http://www.pyfreebilling.com/shop/](http://www.pyfreebilling.com/shop/)

### Donation

If you want to support my developments you are welcome to buy me a cup of coffee :)

[![Paypal donation](static/donate_button_red.jpg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=FANG9JC63Q7DY&lc=FR&item_name=PyFreeBilling&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted)


### Stats

[![Project Stats](https://www.openhub.net/p/pyfreebilling/widgets/project_thin_badge.gif)](https://www.openhub.net/p/pyfreebilling)
