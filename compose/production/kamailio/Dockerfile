FROM debian:9

RUN apt-get update && apt-get install -y kamailio kamailio-postgres-modules kamailio-tls-modules curl tcpdump

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
