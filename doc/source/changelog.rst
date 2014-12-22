Changelog
*********

Version 1.5.0 (Not yet released)
=============

New features
------------

* New CDR import script (PERL packages are no longer needed)
* Recurring services
* Invoicing


Bug corrections
---------------

* N/A


Version 1.4.6
=============

Bug correction
------------

* Resolve a codec error when using Eyebeam as sip client.


Version 1.4.5
=============

Modifications
------------

* Correct javascript issues


Version 1.4.4
=============

Modifications
------------

* Apache template : disable sslv2 and sslv3 (POODLE - CVE-2014-0224)
* Sofia new option : tracelevel with default value "error" (if you need more debug, in cli : sofia tracelevel debug)


Version 1.4.3
=============

New features
------------

* Bd backup every day (in backups directory and FTP)
* Customer panel : new xport CDR panel


Bug corrections
---------------

* fix javascript issues with new firefox version (need delete static before update)
* fix alert message in customer panel when account is blocked due to low balance.
* LUA excaping error in DID
* Fix js bug in inlines (impact LCR and customer view)


Version 1.4.2
=============

New features
------------

* Customer panel traduction (French)
* Add G722 Codec


Bug corrections
---------------

* Admin : stats : div per 0 error
* Test if customer UA has available codec recognised by FS


Version 1.4.1
=============

New features
------------

* Admin stats enhancements

  
Security
--------

* Validation of django 1.6.7 (dependencies update)


Bug corrections
---------------

* Postpaid : a negative credit limit value no longer blocks call process
* Admin : CDR export button is now visible in CDR panel
* Admin : Database size view now correct


Version 1.4
============

New features
------------

* New customer portal
* HTTPS access only
* Reload Fs config via button in admin panel
* Currency management
* Database size monitoring - new panel (in admin menu)
* Sofia Gateway : add new choose lists for selecting codecs
* Add sip profile DTMF options (pass-rfc2833)
* Add new rtp_rewrite_timestamps sofia profile option
* Visitors and web interface use stats
* Admin CDR panel : show minutes / sell / cost / margin corresponding to selection
* New dashboard : revenue / cost / minutes / calls stats
* documentation update for installation of 1.4 freeswitch version
* web country blocker based on visitor's ip. Databases : freegeoip.net and/or maxmind
* detailed customers, providers and destinations stats

Modifications
-------------

* Django 1.6 migration
* All dependencies are up to date
* Optimisation of customer sip parameter and customer sip UA codecs selection

Bug corrections
---------------

* Add new codec options in Customer sip accounts and sip profiles : G711u&G711a and G711a&G711u
* Destination number is checked before LUA
* Recurrent tasks working with new chronicler version


Version 1.3
============

New features
------------

* DID module : import DID, DID billing, DID cdr report
* Customer sip account module : add many options to handle sip registration and NAT. New admin panel.
* Sofia profile module : add many options. New admin panel.
* Add the possibility to block/allow ratecard by CallerID prefix list.

Modifications
-------------

* "Tarif group" is now "ratecard"

Bug corrections
---------------

* some menu corrections
* other bug corrections
