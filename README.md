# P-Kiss-SBC project

![logo](http://www.pyfreebilling.com/wp-content/uploads/2014/12/PyFreeBilling-logo-small.png)

![PyFB release](https://img.shields.io/badge/PKS_version-4.0.0beta-8A2BE2)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/mwolff44/pyfreebilling/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/mwolff44/pyfreebilling/?branch=master)
[![AGPLv3 License](https://img.shields.io/badge/license-AGPLv3-blue.svg?style=flat-square)](http://www.fsf.org)
[![Donate to this project using Paypal](https://img.shields.io/badge/paypal-donate-red.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=FANG9JC63Q7DY&lc=FR&item_name=PyFreeBilling&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted&pk_campaign=donation)

---

## Table of content

- About P-Kiss-SBC
- License
- Features
- Prerequisites
- Installation
- Contact information
- Support
- Contributing
- Donation
- Stats

## What is PKS : P-Kiss-SBC

The new flavor of *pyfreebilling*, P-KISS-SBC, is an *open source simple and stupid SBC* based on *Kamailio* and *RTP Engine* .

## License

P-Kiss-SBC is under AGPLv3 license. You can read it in COPYING file.

[![AGPLv3 License](https://img.shields.io/badge/license-AGPLv3-blue.svg?style=flat-square)](http://www.fsf.org)

## Features

There are some features supported. A few of them are:

- IPBX/Customer add/modify/delete
  - IP termination and SIP authentication (Multitenant system support)
  - DID allocation and routing

- Provider add/modify/delete
  - Routing based on area code
  - DID Routing
  - Routing decision based on load balancing
  - Limit max channels by each provider gateway (TBD)

- Security
  - Blocking SIP scanner attemps
  - Blocking fraudulent connection attempts
  - SQL injection detection
  - SIP header validation

- Design for simplicity, reliability and scalability

... and much more :)

## Prerequisites

In order to run PKS, you need the following configured, secured  and
working Basic Operating System (Linux). P-KISS-SBC works in containers, it can be deployed on any docker or Kubernetes environment.

The project uses Kamailio, RTP Engine, Redis and a Database (by default, POSTGRESQL but also support POSTGRESQL, MARIADB, MYSQL and DBTEXT).

## Contact Information

Name: *Mathias WOLFF*

Contact: [https://blog-des-telecoms.com](https://blog-des-telecoms.com)

Website: [https://pk-sbc.io](https://pk-sbc.io)

## Support

To get free support, use github issue tab.

If you need paid support, specific features or consulting services, you will find support services prices on PyFreeBilling website : [https://pk-sbc.io](https://pk-sbc.io)

## Contributing

Separate proposed changes and PRs into small, distinct patches by type so that they can be merged faster into upstream and released quicker:

- Feature
- Bugfix
- Code style
- Documentation

## Donation

If you want to support my developments you are welcome to offer me a cup of coffee :)

[![Paypal donation](static/donate_button_red.jpg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=FANG9JC63Q7DY&lc=FR&item_name=PyFreeBilling&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted)

## Stats

[![Project Stats](https://www.openhub.net/p/pyfreebilling/widgets/project_thin_badge.gif)](https://www.openhub.net/p/pyfreebilling)
