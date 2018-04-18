# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Next]
### Added
- log sip messages from kamailio into PyFreeBilling DB (acc module)
- New coutntry / directions / prefix matching process

### Changed


### Deprecated


### Removed


### Fixed
- In location DB, typo in cflags fields
- Specify order in DB migration
- Add uacreg and trusted tables for kamailio in PyFreeBilling base

### Security



## [2.1]
### Added
- Kamailio is handled by PyFreeBilling now
- Location table view in PyFB admin

### Changed
- Kamailio configuration has been split
- PostgreSQL min version is 9.4

### Removed
- Currency management, as it not be really used
- Gateway profile as it not used

### Fixed
- Possibility to use a different port form gateways than default
- Many documention points have been fixed

### Security
- Django updated to 1.11.12
- Django-axes updated


## [2.0]
### Added
- Proxy SIP is now Kamailio
- Multi FreeSwitch support (load balancing)
- New translations (managed now on Transifex)
- SIP antiflood protection
- SIP malformed messages detection

### Changed
- CallerID and CalleeID normalization for customers
- Speed up rates and CDR views
- New customers and providers stats
- Better FreeSwitch log messages
- Django 11 based
- PostgreSQL min version is 9.3
- FreeSwitch version : 1.6
- Kamailio version : 4.4
- New licence : AGPL v3

### Deprecated
- Currency maganement (a new one will be replace it)

### Removed
- SIP account authentification in FreeSwitch. It is done in Kamailio now.
- Old DID management system => new one no compatible with the v1.

### Fixed
- Simpler FreeSwitch deployment and configuration
- minimal time in rate now OK

### Security
- Enhance password security : min lenght is 11 characters
- New password storage argon2 (old password will be updated when user log in)

## [1.4.8] - 2016-06-21
### Fixed
- Italian translation

## [1.4.7] - 2016-03-07
## Fixed
- Requirements
- CallerID bug

**Important** : we will keep only 2.0 changelog in the future since 2.0 will be released.  
