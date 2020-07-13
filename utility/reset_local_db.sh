#!/bin/bash
# Resets the local Django database, adding an admin login and migrations
set -e
echo -e "\n>>> Resetting the database"
./manage.py reset_db --close-sessions --noinput

echo -e "\n>>> Running migrations"
./manage.py migrate

echo -e "\n>>> Creating new superuser 'admin'"
./manage.py createsuperuser \
   --username admin \
   --email admin@example.com \
   --noinput

echo -e "\n>>> Setting superuser 'admin' password to 123456"
./manage.py shell_plus --quiet-load -c "
u=User.objects.get(username='admin')
u.set_password('123456')
u.save()
"

# Any extra data setup goes here.

echo -e "\n>>> Database restore finished."

