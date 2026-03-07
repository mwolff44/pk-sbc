<!---
# P-KISS-SBC documentation © 2007-2026 by Mathias WOLFF 
# is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (see https://creativecommons.org/licenses/by-nc-sa/4.0/)
# SPDX-License-Identifier: CC-BY-NC-SA-4.0
--->

# Release Notes

## P-KISS-SBC

### Latest Changes

#### 4.2.0 <small>2026</small> { id="4.2.0" }

**Security**

* Security hardening of the install script (`deploy/pks`): input validation for IP addresses and domain, SHA256 integrity check on downloaded `docker-compose.yml`
* Removed hardcoded fallback password `pa55word` from `docker-compose.yml` — `POSTGRES_PASSWORD` is now mandatory
* Redis authentication support: `REDIS_PASSWORD` generated at install time and propagated to Kamailio
* `pks-rtp` container: replaced `privileged: true` with minimal capabilities (`NET_ADMIN`, `SYS_NICE`)
* Pinned Docker image tags (`caddy:2.8`, versioned images) to prevent tag hijacking
* Patched CVE in SVGO (XXE/entity expansion) via dependency override

**Infrastructure**

* Repository cleaned up: Dockerfiles, Makefile, build artifacts, test fixtures and legacy configs moved to the dedicated build repository
* GitHub Actions workflow replaced: Docker build pipeline removed, new `validate.yml` runs ShellCheck on `deploy/pks` and yamllint on `infra/docker-compose.yml`
* `docker-compose.yml`: removed unused `networks: main` declaration, default `ENVIRONMENT` changed from `dev` to `prod`

**Documentation**

* MkDocs and all plugins updated to latest compatible versions
* Added `Makefile` for venv-based local doc workflow (`make serve`, `make build`, `make test`)
* Jampack upgraded to `0.34.0` and configured for Netlify hosting (image optimization, critical CSS inlining, prefetch)
* Fixed yamllint and ShellCheck CI warnings

---

#### 4.1.4 <small>December 18, 2024</small> { id="4.1.4" }

* Kamailio update: add SDP management for Re-INVITE and reply
* pks-admin update to `1.4.0`: misc updates
* Documentation: primary/secondary setup how-to added

---

#### 4.1.3 <small>November 12, 2024</small> { id="4.1.3" }

* Dockerfile: add `curl` to base image
* pks-admin update to `1.3.1`
* Security: `braces` dependency updated (CVE fix)

---

#### 4.1.2 <small>April 30, 2024</small> { id="4.1.2" }

* Install script: update to always fetch the latest stable version
* Fix: remove R-URI number validation causing routing issues

---

#### 4.1.1 <small>April 18, 2024</small> { id="4.1.1" }

* Fix: error in Kamailio configuration file

---

#### 4.1.0 <small>April 18, 2024</small> { id="4.1.0" }

* pks-admin update to `1.3.0`: call accounting (ACC) reporting added

---

#### 4.0.4 <small>April 18, 2024</small> { id="4.0.4" }

* Fix: bug in external routing rules
* pks-admin update to `1.3.0`: `kamcmd` translate command added, enum fix on rule types

---

#### 4.0.3 <small>April 18, 2024</small> { id="4.0.3" }

* Fix: version mismatch in `pks` script
* Documentation: Docker Hub badges added to README

---

#### 4.0.2 <small>April 16, 2024</small> { id="4.0.2" }

* pks-admin update to `1.2.1`
* Install script: fix Caddy directory creation
* feat: HTTP status endpoint and JSON-RPC API commands added to `pks-sip`
* Documentation: 404 redirects configured

---

#### 4.0.1 <small>March 08, 2024</small> { id="4.0.1" }

* Deployment updated: reverse proxy added for HTTPS (Caddy)
* pks-admin `1.1.0`
* Kamailio update: `5.7.4`

---

#### 4.0.0 <small>March 05, 2024</small> { id="4.0.0" }

First release of P-KISS-SBC.