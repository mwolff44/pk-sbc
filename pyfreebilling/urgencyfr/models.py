# -*- coding: utf-8 -*-
# Copyright 2013 Mathias WOLFF
# This file is part of pyfreebilling.
#
# pyfreebilling is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfreebilling is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfreebilling.  If not, see <http://www.gnu.org/licenses/>

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _


# class Subscriber(models.Model):
#     """ Subscriber table for Kam """
#     id = models.AutoField(auto_created=True, primary_key=True)
#     username = models.CharField(max_length=64)
#     # domain = models.CharField(max_length=64, blank=True)
#     password = models.CharField(max_length=25, blank=True)
#     # email_address = models.CharField(max_length=64, blank=True)
#     # ha1 = models.CharField(max_length=64, blank=True)
#     # ha1b = models.CharField(max_length=64, blank=True)
#     #rpid = models.CharField(max_length=64, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = "subscriber"
#         app_label = "customerdirectory"
#         verbose_name = "Subscriber"
#         verbose_name_plural = "Subscribers"

#     def __str__(self):
#         pass


class InseeCityCode(models.Model):
    """ Insee city code Model """
    insee_code = models.CharField(
        _(u"Code INSEE"),
        max_length=5,
        unique=True,
        help_text=_(u"""Pour les communes appartenant à
            un département dont le code commence par « 0 »,
            il est nécessaire de saisir aussi le code insee
            sur 5 chiffres."""))
    city = models.CharField(
        _(u"Ville"),
        max_length=100)
    new_code = models.CharField(
        _(u"Nouveau Code INSEE"),
        max_length=5,
        blank=True,
        null=True,
        default='',
        help_text=_(u"""Pour les communes appartenant à
            un département dont le code commence par « 0 »,
            il est nécessaire de saisir aussi le code insee
            sur 5 chiffres."""))
    new_date = models.DateTimeField(
        blank=True,
        null=True)
    date_added = models.DateTimeField(
        _(u'date added'),
        auto_now_add=True)
    date_modified = models.DateTimeField(
        _(u'date modified'),
        auto_now=True)

    class Meta:
        db_table = 'urgencyfr-inseecitycode'
        app_label = 'urgencyfr'
        ordering = ('city',)
        verbose_name = _(u'code ville INSEE')
        verbose_name_plural = _(u'code ville INSEE')

    def __unicode__(self):
        return "%s (%s)" % (self.city, self.insee_code)


class UrgencyNumber(models.Model):
    """ Insee city code Model """
    number = models.CharField(
        _(u"Numéro court d\'urgence"),
        max_length=10)
    description = models.CharField(
        _(u"Description"),
        max_length=100)
    date_added = models.DateTimeField(
        _(u'date added'),
        auto_now_add=True)
    date_modified = models.DateTimeField(
        _(u'date modified'),
        auto_now=True)

    class Meta:
        db_table = 'urgencyfr-urgencynumber'
        app_label = 'urgencyfr'
        ordering = ('number', )
        verbose_name = _(u'Numéro court d\'urgence')
        verbose_name_plural = _(u'Numéros court d\'urgence')

    def __unicode__(self):
        return "%s" % (self.number)


class Caau(models.Model):
    """ Insee city code Model """
    caau_code = models.CharField(
        _(u"id CAAU"),
        max_length=10,
        help_text=_(u"""Sigle utilisé pour identifier les centres
            d'accueil des appels d'urgence dans les tableaux.
            Il doit correspondre à la spécification définie par
            le GT399 « logiciel de sécurité civile » qui a défini
            une nomenclature des centres sur 10 caractères."""))
    long_number = models.CharField(
        _(u"Numéro court d\'urgence"),
        max_length=16,
        help_text="""Format E.164 préfixé avec +""")
    new_long_number = models.CharField(
        _(u"Nouveau numéro court d\'urgence"),
        max_length=16,
        blank=True,
        null=True,
        default='',
        help_text="""Format E.164 préfixé avec +""")
    new_date = models.DateTimeField(
        _(u'new date'),
        blank=True,
        null=True)
    enabled = models.BooleanField(
        _(u"Enabled"),
        default=True)
    date_added = models.DateTimeField(
        _(u'date added'),
        auto_now_add=True)
    date_modified = models.DateTimeField(
        _(u'date modified'),
        auto_now=True)

    class Meta:
        db_table = 'urgencyfr-caau'
        app_label = 'urgencyfr'
        ordering = ('caau_code', 'long_number')
        verbose_name = _(u'Centre d\'accueil des appels d\'urgence')
        verbose_name_plural = _(u'Centres d\'accueil des appels d\'urgence')

    def __unicode__(self):
        return "%s (%s)" % (self.caau_code, self.long_number)


class Pdau(models.Model):
    """ Insee city code Model """
    urgencynumber = models.ForeignKey(
        UrgencyNumber,
        verbose_name=_(u"Numéro d\'urgence"),)
    caau = models.ForeignKey(
        Caau,
        related_name="caau",
        verbose_name=_(u"CAAU"),)
    insee_code = models.ForeignKey(
        InseeCityCode,
        verbose_name=_(u"Code INSEE"),)
    new_caau = models.ForeignKey(
        Caau,
        related_name="newcaau",
        null=True,
        blank=True,
        verbose_name=_(u"Nouveau CAAU"),)
    new_date = models.DateTimeField(
        blank=True,
        null=True)
    enabled = models.BooleanField(
        _(u"Enabled"),
        default=True)
    date_added = models.DateTimeField(
        _(u'date added'),
        auto_now_add=True)
    date_modified = models.DateTimeField(
        _(u'date modified'),
        auto_now=True)

    class Meta:
        db_table = 'urgencyfr-pdau'
        app_label = 'urgencyfr'
        ordering = ('insee_code', 'urgencynumber', 'caau')
        verbose_name = _(u'Plan départemental d\'acheminement des appels')
        verbose_name_plural = _(u'Plans départemental d\'acheminement des appels')

    def __unicode__(self):
        return "%s (%s->%s)" % (self.insee_code, self.urgencynumber, self.caau)
