# DOCUMENTATION

## Introduction
The puprose of this document is to describe how to use PyFreeBilling.

### What is PyFreeBilling
PyFreeBilling is an Open Source billing and routing plateform for FreeSwitch.

### Who is this software design for
PyFreeBilling is designed for high performance and scalability. It is suitable for redential, business and wholesale VoIP providers.

## PyFreeBilling installation
The up to date documentation is hosted in [PyFreeBiiling ReadTheDocs](http://pyfreebilling.readthedocs.org/en/latest/).

## Upgrading PyFreeBilling
Just use the upgrade script :

	cd /usr/local/venv
	source bin/activate
	cd pyfreebilling
	fab.py upgrade -v version_number
	
You need to replace version_number by the right number.

## Initial Set-Up

## Security

### Honeypot

#### Introduction
Provide a fake admin login screen to log and notify admins of attempted unauthorized access.

#### Dependencies
Nothing !

#### Settings
If you want admins to be notified by email, you must add in your local_settings.py files these lines :

    ADMIN_HONEYPOT_EMAIL_ADMINS = True
    
The default settings is False.

#### Screenshots

#### To Be implemented
Automatically blocked IP.

For dev, take a look at : admin_honeypot.signals.honeypot()

### Country blocker

#### Introduction
Allow or block web users depending of their IP location.
The module use 2 databases : [freegeoip.net](http://freegeoip.net) and/or maxmind (need subscription <https://geoip.maxmind.com/> )

#### Dependencies
OS packages :

* libgeoip-dev

Python packages :

* RAVEN

* REQUESTS

* GEOIP

#### Default settings
The module is not activate by default.

To activate, you need to add this lines in your local_settings.py file :

    TEMPLATE_CONTEXT_PROCESSORS += (
    'country_block.context_processors.addgeoip',
    )

You need to restart apache server.

#### Files settings
Like others security settings, they are not available in web interface. You have to edit your local_settings.py files.

3 settings have to be set :

* LOCATION : a unique 2 char string that identifies the server's location

* COUNTRY_BLOCK_DEBUG_COUNTRY : sets the user_country equal to this value for all users, letting you test as if you are in this country. False by default.

* COUNTRY_BLOCK_DEBUG_REGION : sets the region_code equal to this value for all users, letting you test as if you are in this region. False by default.

#### Web settings :
* location : This is a unique 2 char value that corresponds to the LOCATION value in the local settings

* free_geo_ip_enabled : Use the freegeoip.net to determine the geography of the user's IP

* free_geo_ip_timeout : freegeoip.net request timeout in seconds (default is 2 seconds)

* maxmind_enabled : Use the https://geoip.maxmind.com/a service to determine the geography of the user's IP. If this is True and free_geo_ip_enabled is also True, the context processor will try the freegeoip.net service first and will only try the Maxmind service if freegeoip.net fails.

* maxmind_timeout : maxmind.com request timeout in seconds (default is 6 seconds)

* maxmind_local_db_enabled : Use a local Maxmind database instead of the https://geoip.maxmind.com/a service. Must also have maxmind_enabled set to True.

* allowed_countries : A M2M relationship of all Countrys that are allowed for the server's location

* staff_user_country : The Country that all django staff users will be assigned

* local_ip_user_country : The Country that all local IP users will be assigned

* maxmind_license_key : The license key for the Maxmind service. A value is required if maxmind_enabled is True and maxmind_local_db_enabled is False. This gets sent over as the 'l' parameter in the payload to the https://geoip.maxmind.com/a service.

#### Screenshots