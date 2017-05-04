#!/bin/sh

#send a message
echo "Install PostgreSQL"

#generate a random password
password=$(dd if=/dev/urandom bs=1 count=20 2>/dev/null | base64)

#Postgres
echo "Install PostgreSQL and create the database and users\n"
apt-get install -y --force-yes sudo postgresql

#systemd
systemctl daemon-reload
systemctl restart postgresql

#init.d
#/usr/sbin/service postgresql restart

#move to /tmp to prevent a red herring error when running sudo with psql
cwd=$(pwd)
cd /tmp
#add the databases, users and grant permissions to them
sudo -u postgres psql -c "CREATE DATABASE pyfreebilling";
sudo -u postgres psql -c "CREATE DATABASE freeswitch";
sudo -u postgres psql -c "CREATE ROLE pyfreebilling WITH SUPERUSER LOGIN PASSWORD '$password';"
sudo -u postgres psql -c "CREATE ROLE freeswitch WITH SUPERUSER LOGIN PASSWORD '$password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE pyfreebilling to pyfreebilling;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE freeswitch to pyfreebilling;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE freeswitch to freeswitch;"
#ALTER USER pyfreebilling WITH PASSWORD 'newpassword';
cd $cwd

#set the ip address
server_address=$(hostname -I)

#Show database password
echo ""
echo ""
echo "PostgreSQL"
echo "   Database name: pyfreebilling"
echo "   Database username: pyfreebilling"
echo "   Database password: $password"
echo ""