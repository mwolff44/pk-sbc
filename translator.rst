Internationalization
====================


This document covers the details regarding internationalization and
localization that are applied in Read the Docs. The guidelines described are
mostly based on `Kitsune's localization documentation
<http://kitsune.readthedocs.io/en/latest/localization.html>`_.

As with most of the Django applications out there, Read the Docs' i18n/l10n
framework is based on `GNU gettext <http://www.gnu.org/software/gettext/>`_.
Crowd-sourced localization is optionally available at `Transifex
<https://www.transifex.com/projects/p/readthedocs/>`_.

For more information about the general ideas,
look at this document: http://www.gnu.org/software/gettext/manual/html_node/Concepts.html


Translate PyFreeBilling Application into your language
------------------------------------------------------

PyFreeBilling language files are already translated in several languages. English is the default and always complete. Other languages depend on contributions. This tutorial can help you complete a translation for a language not yet available or somehow incorrect. PyFreeBilling can be translated by using Transifex platform.


Translating with Transifex
--------------------------

Transifex provides a web-based translation interface, which can be used to translate. Its main features are:

* Web-based, accessible everywhere for anyone, and does not require any developer skill
* Offers a Translation Memory that automatically translates similar terms present in other versions and modules
* Provides collaborative reviewing features, and allows marking the terms that one thinks should be reviewed by other translators
* Automatically synchronized with the source code files (.pot) containing the translations, removing the the need for manual updates

After registering on Transifex, you can access the translations for PyFreeBilling project on the organisation page : <https://www.transifex.com/celea-consulting/pyfreebilling>


Translation teams on Transifex
------------------------------

Every language is managed by a dedicated translation team. Anyone is free to join any translation team at any point. Within each team, members can have different roles:

* Translator: free to join, can submit translation suggestions (this is your role when you initially join a team)
* Reviewer: can approve translation suggestions from Translators
* Coordinator: can manage the members of the team and appoint Reviewers

Translators submit translation suggestions for any language and need the validation of reviewers before their translations are used in PyFreeBilling.

If your language is not yet present in the list of languages and you are motivated enough to manage the team, you can request the addition of this language.

If no Coordinator is assigned to a language team, contact us to require the appointment of a coordinator.

Transifex Integration
^^^^^^^^^^^^^^^^^^^^^

To push updated translation source files to Transifex, run ``tx
push -s`` (for English) or ``tx push -t <language>`` (for non-English).

To pull changes from Transifex, run ``tx pull -a``. Note that Transifex does
not compile the translation files, so you have to do this after the pull.

For more information about the ``tx`` command, read the `Transifex client's
help pages <http://help.transifex.com/features/client/>`_.

More info : `Django Transifex documentaion <https://docs.transifex.com/integrations/django>`_.
