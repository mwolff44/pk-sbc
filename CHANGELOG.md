# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [4.1.4] - 2025-12-18

### Changed
- Kamailio and pks-admin updates
- npm dependencies update
- Clean up package.json by removing unused entries

### Added
- SDP management for Re-Invite and reply

## [4.1.3] - 2024-11-12

### Added
- Dockerfile: add curl

### Changed
- Update pks-admin to 1.3.1
- Documentation: primary/secondary setup

### Fixed
- Dependabot alert: braces update

## [4.1.2] - 2024-04-30

### Changed
- Remove validation on R-URI number
- Update install to latest version

## [4.1.1] - 2024-04-18

### Fixed
- pks-sip: error in config file

## [4.1.0] - 2024-04-18

### Added
- pks-admin: acc reporting (CDR)

## [4.0.4] - 2024-04-18

### Added
- pks-admin: update to 1.3.0, kamcmd translate added

### Fixed
- pks-sip: bug in external routing
- pks-admin: type of rules, error in enum

## [4.0.3] - 2024-04-18

### Fixed
- pks script: fix version

### Changed
- README: add Docker badges

## [4.0.2] - 2024-04-16

### Added
- pks-sip: add status endpoint and API commands

### Fixed
- pks-admin: update to 1.2.1
- pks install typo

### Changed
- Update Caddy volume and directories

## [4.0.1] - 2024-03-08

### Added
- HTTPS proxy support (Caddy)

### Changed
- Docker and CI updates
- Install script improvements

## [4.0.0] - 2024-03-05

### Added
- Full Docker Compose orchestration (pks-sip, pks-rtp, pks-redis, pks-db, pks-admin, pks-proxy)
- pks CLI for managing the solution (install, start, stop, reload, debug, DB viewer)
- Resource usage statistics in CLI
- Version check in CLI
- Documentation site with MkDocs Material

### Changed
- Complete rewrite as a containerized SBC
- Kamailio 5.7.6 based SIP proxy
- PostgreSQL 16 as default database
- New web administration interface (pks-admin)

### Removed
- All legacy PyFreeBilling components

## [PKS-1.0.0]

### Added
- Connect IPBX and provider SIP trunks - only IP auth are supported
- DID routing
- PSTN routing
- Loadbalancing routing features
- Commandline to manage the solution

### Changed
- New version dropping ratings to focus on security

### Removed
- PyFreeBilling v2 features are removed
