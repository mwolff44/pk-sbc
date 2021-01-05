# -*- coding: utf-8 -*-
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_countries import countries
from django_countries.fields import CountryField
from django_extensions.db import fields as extension_fields
from django_extensions.db.fields import AutoSlugField
from model_utils.models import TimeStampedModel


class Carrier(TimeStampedModel):

    # Fields
    name = models.CharField(_(u"carrier name"), max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name', blank=True)

    class Meta:
        db_table = 'pyfb_direction_carrier'
        ordering = ('name',)

    def __str__(self):
        return u'%s' % self.name

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('pyfb-direction:pyfb-direction_carrier_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('pyfb-direction:pyfb-direction_carrier_update', args=(self.slug,))


class Type(TimeStampedModel):

    # Fields
    name = models.CharField(_(u"type of destination"), max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name', blank=True)

    class Meta:
        db_table = 'pyfb_direction_type'
        ordering = ('name',)

    def __str__(self):
        return u'%s' % self.name

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('pyfb-direction:pyfb-direction_type_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('pyfb-direction:pyfb-direction_type_update', args=(self.slug,))


class Region(TimeStampedModel):

    # Fields
    name = models.CharField(_(u"region name"), max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name', blank=True)

    class Meta:
        db_table = 'pyfb_direction_region'
        ordering = ('name',)

    def __str__(self):
        return u'%s' % self.name

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('pyfb-direction:pyfb-direction_region_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('pyfb-direction:pyfb-direction_region_update', args=(self.slug,))


class Risk(TimeStampedModel):

    # Fields
    name = models.CharField(_(u"Risk evaluation"), max_length=255, unique=True)

    class Meta:
        db_table = 'pyfb_direction_risk'
        ordering = ('pk',)

    def __str__(self):
        return u'%s' % self.name

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('pyfb-direction:pyfb-direction_risk_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('pyfb-direction:pyfb-direction_risk_update', args=(self.slug,))


class Country(TimeStampedModel):

    # Fields
    country_iso2 = CountryField(_(u"country"), unique=True)

    # Relationship Fields
    region = models.ForeignKey(Region,
        verbose_name=_(u"region"), on_delete=models.SET_NULL, blank=True, null=True,
    )
    # Risk evaluation
    risk = models.ForeignKey(Risk,
        verbose_name=_(u"risk evaluation"), on_delete=models.SET_NULL, blank=True, null=True,
    )


    class Meta:
        db_table = 'pyfb_direction_country'
        ordering = ('country_iso2',)

    def __str__(self):
        return u'%s' % self.country_iso2

    def __unicode__(self):
        return u'%s' % self.country_iso2

    def get_absolute_url(self):
        return reverse('pyfb-direction:pyfb-direction_country_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-direction:pyfb-direction_country_update', args=(self.pk,))


class Destination(TimeStampedModel):

    # Fields
    name = models.CharField(_(u"name of destination"), max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name', blank=True)
    # country_iso2 = CountryField(_(u"country"), blank=True)

    # Relationship Fields
    country_iso2 = models.ForeignKey(Country,
        verbose_name=_(u"country"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        to_field='country_iso2',
    )
    carrier = models.ForeignKey(Carrier,
        verbose_name=_(u"carrier"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    type = models.ForeignKey(Type,
        verbose_name=_(u"Type of destination"), on_delete=models.PROTECT
    )

    class Meta:
        db_table = 'pyfb_direction_destination'
        ordering = ('name',)

    def country(self):
        return countries.name(self.country_iso2)

    def __str__(self):
        return u'%s' % self.name

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('pyfb-direction:pyfb-direction_destination_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('pyfb-direction:pyfb-direction_destination_update', args=(self.slug,))


class Prefix(TimeStampedModel):

    # Fields
    prefix = models.CharField(_(u"prefix"), unique=True, max_length=15, help_text=_(u"International public telecommunication prefix (maximum 15 digits)"))
    slug = AutoSlugField(populate_from='prefix', blank=True)

    # Relationship Fields
    destination = models.ForeignKey(Destination,
        verbose_name=_(u"destination"), on_delete=models.PROTECT,
    )

    class Meta:
        db_table = 'pyfb_direction_prefix'
        ordering = ('prefix',)

    def __str__(self):
        return u'%s' % self.prefix

    def __unicode__(self):
        return u'%s' % self.prefix

    def get_absolute_url(self):
        return reverse('pyfb-direction:pyfb-direction_prefix_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('pyfb-direction:pyfb-direction_prefix_update', args=(self.slug,))
