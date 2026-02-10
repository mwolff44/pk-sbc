# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

P-KISS-SBC is an open-source SIP Border Controller (SBC) built on **Kamailio 5.7.6** and **RTP Engine**. It interconnects IPBXs and telecom operators, providing SIP routing, security, load balancing, and multi-tenant support. Licensed under AGPLv3.

## Architecture

The system runs as a set of Docker containers orchestrated via Docker Compose:

- **pks-sip** — Kamailio-based SIP proxy (core component). Configuration in `infra/kamailio.cfg`.
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
| `infra/kamailio.cfg` | Main Kamailio SIP proxy configuration (~700 lines) |
| `infra/bootstrap.sh` | Container entrypoint — generates `kamailio-local.cfg` from environment variables, detects cloud provider IPs, validates config, launches Kamailio |
| `deploy/pks` | Bash CLI for managing PKS (install, start, stop, reload, debug, DB viewer) |
| `infra/docker-compose.yml` | Full stack orchestration |
| `Dockerfile` | Main Docker image (Debian Bookworm + Kamailio 5.7.6) |

### Configuration System

Kamailio uses a two-layer config approach:
- `kamailio.cfg` — static main config with `#!define` preprocessor directives and defaults
- `kamailio-local.cfg` — generated at container startup by `bootstrap.sh` from environment variables (`LISTEN_PUBLIC`, `LISTEN_PRIVATE`, `LISTEN_ADVERTISE`, `DB_PGSQL`/`DB_MYSQL`/`DB_SQLITE`, `RTPENGINE_URL`, `REDIS_URL`, `ANTIFLOOD`, etc.)

Database backend is selected by which `DB_*` env var is set; falls back to DBTEXT (flat files) if none.

### Database Tables

Core tables: `address` (IP auth), `dialplan` (routing rules), `dispatcher` (gateways), `htable` (tenant mapping), `acc`/`acc_cdrs` (call accounting), `domain`, `dialog`, `rtpengine`.

Schemas live in `infra/db/{postgresql,mysql,sqlite}/` with DBTEXT definitions as `.txt` files in `infra/db/`.

## Build & Development Commands

All Docker Compose commands run from `infra/` and require `/srv/pks/.env` plus `infra/.envrc`.

```bash
# Validate Kamailio config syntax (builds a test container)
make -C infra check/proxy

# Build all containers
make -C infra build/proxy

# Start / stop / restart the full stack
make -C infra run/proxy
make -C infra stop/proxy
make -C infra restart/proxy

# Start / stop just the SIP proxy
make -C infra run/sipproxy
make -C infra stop/sipproxy

# View logs
make -C infra logs/proxy

# Container status
make -C infra ps/proxy
```

The `deploy/pks` CLI wraps Docker operations for production use:
```bash
deploy/pks start | stop | restart
deploy/pks -r          # reload config tables (address, dialplan, tenant, dispatcher)
deploy/pks -d          # live debug logs
deploy/pks -s          # container status
deploy/pks db          # interactive DB viewer
```

## Testing

BDD-style tests in `infra/tests/` use Gherkin `.feature` files and the `voip_patrol` tool:

```bash
# Run SIP call tests (requires a running stack + voip_patrol)
VOIP_DOMAIN=dev-voip.com FROM_CALLER=+33613000014 TOKEN_TEST=... USER_ID_TEST=... infra/tests/test.sh
```

Tests iterate over SIP response codes (403, 404, 408, 486, 487, 503, 200), making calls and verifying expected responses. Test DB fixtures are in `infra/tests/db-test/`.

## CI/CD

GitHub Actions (`.github/workflows/docker-image.yml`):
- **On push to main / tags / PRs**: builds the Docker image (`linux/amd64`)
- **On non-PR events**: pushes to Docker Hub as `mwolff44w/pks-sipproxy` with semver + SHA tags
- Uses BuildX with GitHub Actions cache, generates SBOM/provenance on releases

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

Per `.editorconfig`:
- UTF-8, LF line endings, final newline required
- Kamailio `.cfg` files and Bash scripts: follow existing indentation patterns
- Python: 4-space indent, 120 char line length
- YAML/JSON: 2-space indent
