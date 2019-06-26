FROM debian:9

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
