FROM debian:9

MAINTAINER Mathias WOLFF <mathias@celea.org>

# Important! Update this no-op ENV variable when this Dockerfile
# is updated with the current date. It will force refresh of all
# of the base images and things like 'apt-get update' won't be using
# old cached versions when the Dockerfile is built.
ENV REFRESHED_AT 2019-07-17

RUN apt-get update && apt-get install -y wget gnupg

RUN echo "deb http://deb.kamailio.org/kamailio52 stretch main" > /etc/apt/sources.list.d/kamailio.list
RUN wget -O- http://deb.kamailio.org/kamailiodebkey.gpg | apt-key add -

RUN apt-get update && apt-get install -y kamailio kamailio-extra-modules kamailio-outbound-modules kamailio-postgres-modules kamailio-tls-modules kamailio-redis-modules kamailio-xml-modules curl tcpdump

#setup dumb-init
RUN curl -k -L https://github.com/Yelp/dumb-init/releases/download/v1.2.1/dumb-init_1.2.1_amd64 > /usr/bin/dumb-init
RUN chmod 755 /usr/bin/dumb-init

# Config files.
ADD ./setup/kamailio/etc /etc/kamailio

ADD ./compose/production/kamailio/run.sh /run.sh
RUN chmod +x /run.sh
RUN touch /env.sh
ENTRYPOINT ["/run.sh"]
CMD ["/usr/sbin/kamailio", "-DD", "-P", "/var/run/kamailio.pid", "-f", "/etc/kamailio/kamailio.cfg"]
