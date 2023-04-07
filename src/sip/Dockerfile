FROM debian:bullseye

MAINTAINER Mathias WOLFF <mathias@celea.org>

# Important! Update this no-op ENV variable when this Dockerfile
# is updated with the current date. It will force refresh of all
# of the base images and things like 'apt-get update' won't be using
# old cached versions when the Dockerfile is built.
ENV REFRESHED_AT 2022-08-01
ENV VERSION 1.0.0

ENV KAMAILIO_LOG_LEVEL info

# avoid httpredir errors
RUN sed -i 's/httpredir/deb/g' /etc/apt/sources.list

RUN rm -rf /var/lib/apt/lists/* && apt-get update && apt-get install --assume-yes gnupg wget

# kamailio repo
RUN echo "deb http://deb.kamailio.org/kamailio56 bullseye main" >   /etc/apt/sources.list.d/kamailio.list
RUN wget -O- http://deb.kamailio.org/kamailiodebkey.gpg | apt-key add -

RUN apt-get update && apt-get install --assume-yes \
kamailio \
kamailio-extra-modules \
kamailio-json-modules \
kamailio-utils-modules \
kamailio-xml-modules

# clean
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Add DB
VOLUME ["/etc/kamailio", "/db"]

ENTRYPOINT ["/usr/sbin/kamailio", "-DD", "-P", "/var/run/kamailio.pid", "-f", "/etc/kamailio/kamailio.cfg"]
