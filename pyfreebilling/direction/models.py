# Copyright 2018 Mathias WOLFF
# This file is part of pyfreebilling.
#
# pyfreebilling is free software: you can redistribute it and/or modify
# it under the terms of the Affero GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfreebilling is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pyfreebilling.  If not, see <http://www.gnu.org/licenses/>

from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.db import models as models
from django.db.models import *
from django.utils.translation import ugettext_lazy as _

from django_countries.fields import CountryField
from django_extensions.db import fields as extension_fields
from django_extensions.db.fields import AutoSlugField


class Carrier(models.Model):

    # Fields
    name = models.CharField(_(u"carrier name"), max_length=255, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)


    class Meta:
        db_table = 'dest_carrier'
        app_label = 'direction'
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('direction_carrier_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('direction_carrier_update', args=(self.slug,))


class Type(models.Model):

    # Fields
    name = models.CharField(_(u"type of destination"), max_length=255, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)


    class Meta:
        db_table = 'dest_type'
        app_label = 'direction'
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('direction_type_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('direction_type_update', args=(self.slug,))


class Destination(models.Model):

    # Fields
    name = models.CharField(_(u"name of destination"), max_length=255, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    country_iso2 = CountryField(_(u"country"), blank=True)

    # Relationship Fields
    carrier = models.ForeignKey(Carrier,
        verbose_name=_(u"carrier"), on_delete=models.PROTECT
    )
    type = models.ForeignKey(Type,
        verbose_name=_(u"Type of destination"), on_delete=models.PROTECT
    )

    class Meta:
        db_table = 'dest_destination'
        app_label = 'direction'
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('direction_destination_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('direction_destination_update', args=(self.slug,))


class Prefix(models.Model):

    # Fields
    prefix = models.CharField(_(u"prefix"), unique=True, max_length=15, help_text=_(u"International public telecommunication prefix (maximum 15 digits)"))
    slug = extension_fields.AutoSlugField(populate_from='prefix', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    # Relationship Fields
    destination = models.ForeignKey(Destination,
        verbose_name=_(u"destination"), on_delete=models.PROTECT,
    )

    class Meta:
        db_table = 'dest_prefix'
        app_label = 'direction'
        ordering = ('prefix',)

    def __unicode__(self):
        return u'%s' % self.prefix

    def get_absolute_url(self):
        return reverse('direction_prefix_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('direction_prefix_update', args=(self.slug,))


class Region(models.Model):

    # Fields
    name = models.CharField(_(u"region name"), max_length=255, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = 'dest_region'
        app_label = 'direction'
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('direction_region_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('direction_region_update', args=(self.slug,))


class Country(models.Model):

    # Fields
    country_iso2 = CountryField(_(u"country"), unique=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    # Relationship Fields
    region = models.ForeignKey(Region,
        verbose_name=_(u"region"), on_delete=models.SET_NULL, blank=True, null=True,
    )

    class Meta:
        db_table = 'dest_country'
        app_label = 'direction'
        ordering = ('country_iso2',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('direction_country_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('direction_country_update', args=(self.pk,))
