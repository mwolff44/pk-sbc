# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

P-KISS-SBC is an open-source SIP Border Controller (SBC) built on **Kamailio 5.7.6** and **RTP Engine**. It interconnects IPBXs and telecom operators, providing SIP routing, security, load balancing, and multi-tenant support. Licensed under AGPLv3.

## Architecture

The system runs as a set of Docker containers orchestrated via Docker Compose:

- **pks-sip** — Kamailio-based SIP proxy (core component). Image built and maintained in a separate repository.
- **pks-rtp** — RTP Engine for media relay.
- **pks-redis** — Redis for caching/session state.
- **pks-db** — PostgreSQL 16 (also supports MySQL, SQLite, DBTEXT).
- **pks-admin** — Web administration interface.
- **pks-proxy** — Caddy reverse proxy for HTTPS.

### Call Flow

1. **Authentication** — Source IP checked against the `address` table.
2. **Routing** — DID/outbound destination resolved via the `dialplan` module.
3. **Gateway selection** — `dispatcher` module picks a target gateway (round-robin by default).
4. **Media** — RTP Engine handles media relay between parties.

### Key Source Files

| File | Purpose |
|---|---|
| `deploy/pks` | Bash CLI for managing PKS (install, start, stop, reload, debug, DB viewer) |
| `infra/docker-compose.yml` | Full stack orchestration — downloaded to `/srv/pks/` on install |
| `infra/template.kamailio-local.cfg` | Reference template for Kamailio local config options |
| `infra/cron/pks` | Cron job example for scheduled reloads |

### Configuration System

Kamailio uses a two-layer config approach (managed inside the Docker image):
- `kamailio.cfg` — static main config with `#!define` preprocessor directives and defaults (lives in the build repo)
- `kamailio-local.cfg` — generated at container startup from environment variables (`LISTEN_PUBLIC`, `LISTEN_PRIVATE`, `LISTEN_ADVERTISE`, `DB_PGSQL`/`DB_MYSQL`/`DB_SQLITE`, `RTPENGINE_URL`, `REDIS_URL`, `ANTIFLOOD`, etc.)

See `infra/template.kamailio-local.cfg` for available options. Database backend is selected by which `DB_*` env var is set; falls back to DBTEXT (flat files) if none.

### Database Tables

Core tables: `address` (IP auth), `dialplan` (routing rules), `dispatcher` (gateways), `htable` (tenant mapping), `acc`/`acc_cdrs` (call accounting), `domain`, `dialog`, `rtpengine`.

## Managing PKS

The `deploy/pks` CLI is the sole management tool for production use. It operates on `/srv/pks/docker-compose.yml` (downloaded from this repo during install) and `/srv/pks/.env`.

```bash
deploy/pks install     # first-time installation
deploy/pks start | stop | restart
deploy/pks -r          # reload config tables (address, dialplan, tenant, dispatcher)
deploy/pks -d          # live debug logs
deploy/pks -s          # container status
deploy/pks db          # interactive DB viewer
deploy/pks update      # pull latest images and restart
deploy/pks uninstall   # remove all containers and data
```

## CI/CD

GitHub Actions (`.github/workflows/validate.yml`):
- **On push to main / PRs**: runs ShellCheck on `deploy/pks` and yamllint on `infra/docker-compose.yml`
- Docker image builds are handled in a separate repository; images are published to Docker Hub as `mwolff44w/pks-sipproxy`

## Documentation

Built with MkDocs + Material theme. Bilingual (English/French) with suffix-based i18n.

```bash
pip install -r requirements.txt
mkdocs serve        # local preview
mkdocs build        # build to site/
npm run optimize    # optimize built site with jampack
```

Deployed to Netlify automatically. Docs source is in `docs/`.

## Code Style

Code style conventions:
- UTF-8, LF line endings, final newline required
- Bash scripts: follow existing indentation patterns
- YAML/JSON: 2-space indent
