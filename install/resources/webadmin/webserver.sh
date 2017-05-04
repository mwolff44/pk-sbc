#!/bin/sh

#send a message
echo "Install the web server\n"

#install dependencies
apt-get install -y --force-yes nginx php5 php5-cli php5-fpm php5-pgsql php5-sqlite php5-odbc php5-curl php5-imap php5-mcrypt

#enable pyfreebilling nginx config
cp resources/nginx/pyfreebilling /etc/nginx/sites-available/pyfreebilling
ln -s /etc/nginx/sites-available/pyfreebilling /etc/nginx/sites-enabled/pyfreebilling

#self signed certificate
ln -s /etc/ssl/private/ssl-cert-snakeoil.key /etc/ssl/private/nginx.key
ln -s /etc/ssl/certs/ssl-cert-snakeoil.pem /etc/ssl/certs/nginx.crt

#remove the default site
rm /etc/nginx/sites-enabled/default