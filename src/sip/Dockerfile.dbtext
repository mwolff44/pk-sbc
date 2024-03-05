FROM debian:bullseye

MAINTAINER Mathias WOLFF <mathias@celea.org>

ENV REFRESHED_AT 2023-04-29
ENV VERSION 1.0.1

ENV DEBIAN_FRONTEND noninteractive

ENV DIST="bullseye"
ENV REL="56"

ENV KAMAILIO_LOG_LEVEL info

# avoid httpredir errors
RUN sed -i 's/httpredir/deb/g' /etc/apt/sources.list

RUN rm -rf /var/lib/apt/lists/* && apt-get update && apt-get install --assume-yes gnupg wget iproute2

# kamailio repo
RUN echo "deb http://deb.kamailio.org/kamailio$REL $DIST main" >   /etc/apt/sources.list.d/kamailio.list
RUN wget -O- http://deb.kamailio.org/kamailiodebkey.gpg | apt-key add -

RUN apt-get update && apt-get install --assume-yes \
libhiredis0.14 \
kamailio \
kamailio-extra-modules \
kamailio-json-modules \
kamailio-utils-modules \
kamailio-redis-modules \
kamailio-xml-modules

# clean
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ./kamailio.cfg /etc/kamailio/kamailio.cfg
COPY ./bootstrap.sh /etc/kamailio/bootstrap.sh
RUN chmod a+x /etc/kamailio/bootstrap.sh

ENTRYPOINT ["/etc/kamailio/bootstrap.sh"]
CMD ["kamailio"]

HEALTHCHECK CMD curl --fail http://localhost:8080/ping || exit 1
