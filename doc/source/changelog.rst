Changelog
*********

Version 1.4
============

New features
------------

* New customer portal
* HTTPS access only
* Reload Fs config via button in admin panel
* Currency management
* Database size monitoring - new panel (in admin menu)
* Sofia Gateway : add new chooce lists for selecting codecs
* Add sip profile DTMF options (pass-rfc2833)
* Add new rtp_rewrite_timestamps sofia profile option
* Visitors and web interface use stats
* Admin CDR panel : show minutes / sell / cost / margin corresponding to selection
* New dashboard : revenue / cost / minutes / calls stats
* documentation update for installation of 1.4 freeswitch version

Modifications
-------------

* Django 1.6 migration
* All dependencies are up to date
* Optimisation of customer sip parameter and customer sip UA codecs selection

Bug corrections
---------------

* Add new codec options in Customer sip accounts and sip profiles : G711u&G711a and G711a&G711u
* Destination number is checked before LUA


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
