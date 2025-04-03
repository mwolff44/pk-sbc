# Copyright: (c) 2007-2025 Mathias WOLFF (mathias@celea.org)
# GNU Affero General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/agpl-3.0.txt)
# SPDX-License-Identifier: AGPL-3.0-or-later

FROM debian:bookworm-slim

LABEL org.opencontainers.image.authors Mathias WOLFF <mathias@celea.org>

ENV REFRESHED_AT 2025-04-03
ENV VERSION 4.2.0

ENV DEBIAN_FRONTEND noninteractive

ENV DIST="bookworm"
ENV REL="5.7.6"

ENV KAMAILIO_LOG_LEVEL info

RUN rm -rf /var/lib/apt/lists/* && apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -qq --assume-yes gnupg wget curl apt-transport-https

# kamailio repo
RUN echo "deb http://deb-archive.kamailio.org/repos/kamailio-$REL $DIST main" >   /etc/apt/sources.list.d/kamailio.list
RUN wget -O /tmp/kamailiodebkey.gpg http://deb.kamailio.org/kamailiodebkey.gpg \
  && gpg --output /etc/apt/trusted.gpg.d/deb-kamailio-org.gpg --dearmor /tmp/kamailiodebkey.gpg


RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -qq --assume-yes \
  libhiredis0.14 \
  libpq5 \
  kamailio \
  kamailio-extra-modules \
  kamailio-json-modules \
  kamailio-utils-modules \
  kamailio-redis-modules \
  kamailio-xml-modules \
  kamailio-postgres-modules

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY src/sip/kamailio.cfg /etc/kamailio/kamailio.cfg
COPY src/sip/bootstrap.sh /etc/kamailio/bootstrap.sh
RUN chmod a+x /etc/kamailio/bootstrap.sh

ENTRYPOINT ["/etc/kamailio/bootstrap.sh"]
CMD ["kamailio"]

HEALTHCHECK CMD curl --fail http://localhost:8080/ping || exit 1
