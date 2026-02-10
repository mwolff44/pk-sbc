FROM debian:bullseye

COPY ./modules.conf /modules.conf

RUN apt-get update && \
DEBIAN_FRONTEND=noninteractive apt-get -y install git build-essential pkg-config uuid-dev zlib1g-dev libjpeg-dev libsqlite3-dev libcurl4-openssl-dev libpcre3-dev libspeexdsp-dev libldns-dev libedit-dev libtiff5-dev yasm libopus-dev libsndfile1-dev unzip libavformat-dev libswscale-dev libavresample-dev liblua5.2-dev liblua5.2-0 cmake libpq-dev unixodbc-dev autoconf automake ntpdate libxml2-dev libpq-dev libpq5 &&\
\
cd /usr/src/ && \
git clone https://github.com/signalwire/libks.git && \
cd libks && \
cmake . && \
make && make install && \
\
cd /usr/src/ && \
git clone https://github.com/signalwire/signalwire-c.git && \
cd signalwire-c && \
cmake . && \
make && make install && \
\
cd /usr/src/ && \
git clone https://github.com/freeswitch/sofia-sip.git && \
cd sofia-sip && \
./bootstrap.sh && \
./configure && \
make && make install && \
\
cd /usr/src/ && \
git clone https://github.com/freeswitch/spandsp.git && \
cd spandsp && \
./bootstrap.sh && \
./configure && \
make && make install && \
\
ldconfig && \
\
cd /usr/src/ && \
git clone https://github.com/signalwire/freeswitch.git -bv1.10 freeswitch && \
cd freeswitch && \
git config pull.rebase true && \
#Here you can build your Freeswitch on specific commit, it is allways good practice to do so
#git checkout f9990221e6094886066ec2bf9685648135bd405a && \
#git checkout v1.10.8 && \
cp /modules.conf /usr/src/freeswitch/modules.conf && \
\
./bootstrap.sh -j && \
./configure && \
make && \
make install

CMD ["/usr/local/freeswitch/bin/freeswitch", "-nonat"]