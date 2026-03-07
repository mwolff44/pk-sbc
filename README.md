# P-KISS-SBC

![PKS release](https://img.shields.io/badge/PKS_version-4.2.0-8A2BE2)
![Docker pks-sipproxy Pulls](https://img.shields.io/docker/pulls/mwolff44w/pks-sipproxy)
[![AGPLv3 License](https://img.shields.io/badge/license-AGPLv3-blue.svg?style=flat-square)](http://www.fsf.org)

---

## What is P-KISS-SBC

P-KISS-SBC is an open source, simple SIP Border Controller (SBC) built on **Kamailio**, **RTP Engine**, **Redis** and **PostgreSQL**. It interconnects IPBXs and telecom operators with SIP routing, security and multi-tenant support.

## Features

- **IPBX / Customer management**
  - IP termination and SIP authentication
  - Multi-tenant support
  - DID allocation and routing

- **Provider management**
  - Routing based on area code
  - DID routing
  - Load-balanced gateway selection

- **Security**
  - SIP scanner blocking
  - Fraudulent connection attempt blocking
  - SQL injection detection
  - SIP header validation

- **Design** — simplicity, reliability and scalability

## Quick Start

```bash
git clone https://github.com/mwolff44/pk-sbc.git
cd pk-sbc
deploy/pks install
deploy/pks start
```

See the full documentation for environment configuration and advanced setup.

## Documentation

[https://pk-sbc.io](https://pk-sbc.io)

## Contributing

Separate proposed changes and PRs into small, distinct patches by type so that they can be merged faster into upstream and released quicker:

- Feature
- Bugfix
- Code style
- Documentation

## Support

For free support, use the [GitHub issues](https://github.com/mwolff44/pk-sbc/issues) tab.

For paid support, specific features or consulting services, contact [CELEA Consulting](https://celea.org).

## Author

Created and maintained by [Mathias WOLFF](https://www.linkedin.com/in/mathias-wolff-47a7941/).

## Donation

If you want to support the project, you are welcome to offer a cup of coffee :)

[![Donate to this project using Paypal](https://img.shields.io/badge/paypal-donate-red.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=FANG9JC63Q7DY&lc=FR&item_name=P-KISS-SBC&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHosted)
