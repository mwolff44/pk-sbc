# -*- coding: utf-8 -*-
from django.core.validators import MaxValueValidator
from django.urls import reverse
from django.db import models as models
from django.db.models import *
from django.contrib.postgres.fields import DateTimeRangeField
from django.utils.translation import ugettext_lazy as _

from django_extensions.db import fields as extension_fields
from django_extensions.db.fields import AutoSlugField

from model_utils.models import StatusModel, TimeStampedModel
from model_utils import Choices

from partial_index import PartialIndex

from pyfb_direction.models import Country, Destination, Region, Type
from pyfb_endpoint.models import ProviderEndpoint
from pyfb_rating.models import ProviderRatecard
from pyfb_company.models import Customer


class RoutingGroup(StatusModel, TimeStampedModel):

    # Choices
    STATUS = Choices(
        ('enabled', _(u"Enabled")),
        ('disabled', _(u"Disabled")),
    )

    # Fields
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(_(u'description'), blank=True)


    class Meta:
        db_table = 'pyfb_routing_routinggroup'
        ordering = ('name',)

    def __str__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('pyfb-routing:route_routinggroup_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('pyfb-routing:route_routinggroup_update', args=(self.slug,))


class CustomerRoutingGroup(TimeStampedModel):
    """ Customer routing group Model """

    # Fields
    description = models.CharField(_(u'Comment'), max_length=30, blank=True)

     # Relationship Fields
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_(u"customer"))
    routinggroup = models.ForeignKey(RoutingGroup, on_delete=models.CASCADE, verbose_name=_(u"routing group"))

    class Meta:
        db_table = 'pyfb_routing_c_routinggrp'
        ordering = ('customer', 'routinggroup')
        unique_together = [
            ['customer', 'routinggroup'],
        ]
        verbose_name = _(u'Customer Routing group Allocation')
        verbose_name_plural = _(u'Customer routing group Allocations')

    def __str__(self):
        return u"%s - %s" % (self.customer, self.routinggroup)

    def get_absolute_url(self):
        return reverse('pyfb-routing:pyfb_routing_customerroutinggroup_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-routing:pyfb_routing_customerroutinggroup_update', args=(self.pk,))


class RuleModel(models.Model):

    # Choices
    LCR_TYPE_CHOICES = Choices(
        ('LCR', _(u"Least cost")),
        ('PRIO', _(u"Priority")),
        ('WEIGHT', _(u"Weight")),
        ('QUALITY', _(u"Quality")),
    )
    STATUS_CHOICES = Choices(
        ('enabled', _(u"Enabled")),
        ('disabled', _(u"Disabled")),
        ('blocked', _(u"Blocked")),
    )

    # Fields
    status = models.CharField(_(u"Status"), max_length=20, default=STATUS_CHOICES.enabled, choices=STATUS_CHOICES, help_text=_(u"State of the rate : enabled / blocked - calls to this destination are blocked / disabled"))
    route_type = models.CharField(_(u"route type"), max_length=10, choices=LCR_TYPE_CHOICES, default=LCR_TYPE_CHOICES.LCR)
    weight = models.PositiveIntegerField(default=1)
    priority = models.PositiveIntegerField(default=1)

    # Relationship Fields
    provider_ratecard = models.ForeignKey(
        ProviderRatecard,
        on_delete=models.PROTECT
    )
    provider_gateway_list = models.ManyToManyField(
        ProviderEndpoint,
        #limit_choices_to={'ProviderEndpoint__provider': provider_ratecard__provider},
    ) # filter by provider

    class Meta:
        abstract = True


class PrefixRule(TimeStampedModel, RuleModel):

    # Fields
    prefix = models.CharField(_(u'numeric prefix'), max_length=30, db_index=True)
    destnum_length = models.PositiveSmallIntegerField(_(u'Destination number length'), default=0, help_text=_(u"If value > 0, then destination number must match tsi length"))

    # Relationship Fields
    c_route = models.ForeignKey(RoutingGroup, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pyfb_routing_prefix_rule'
        ordering = ('prefix', '-destnum_length')
        unique_together = [
            ['c_route', 'prefix', 'destnum_length', 'provider_ratecard'],
        ]
        indexes = [
            PartialIndex(
                fields=['c_route', 'prefix', 'destnum_length', 'provider_ratecard'],
                unique=True,
                where='status <> \'disabled\''
            ),
        ]

    def __str__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-routing:route_prefixrule_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-routing:route_prefixrule_update', args=(self.pk,))


class DestinationRule(TimeStampedModel, RuleModel):


    # Relationship Fields
    c_route = models.ForeignKey(RoutingGroup, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pyfb_routing_destination_rule'
        ordering = ('destination',)
        unique_together = [
            ['c_route', 'destination', 'provider_ratecard'],
        ]
        indexes = [
            PartialIndex(
                fields=['c_route', 'destination', 'provider_ratecard'],
                unique=True,
                where='status <> \'disabled\''
            ),
        ]

    def __str__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-routing:route_destinationrule_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-routing:route_destinationrule_update', args=(self.pk,))


class CountryTypeRule(TimeStampedModel, RuleModel):


    # Relationship Fields
    c_route = models.ForeignKey(RoutingGroup, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pyfb_routing_countrytype_rule'
        ordering = ('country', 'type')
        unique_together = [
            ['c_route', 'country', 'type', 'provider_ratecard'],
        ]
        indexes = [
            PartialIndex(
                fields=['c_route', 'country', 'type', 'provider_ratecard'],
                unique=True,
                where='status <> \'disabled\''
            ),
        ]

    def __str__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-routing:route_countrytyperule_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-routing:route_countrytyperule_update', args=(self.pk,))


class CountryRule(TimeStampedModel, RuleModel):


    # Relationship Fields
    c_route = models.ForeignKey(RoutingGroup, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pyfb_routing_countryrule'
        ordering = ('country',)
        unique_together = [
            ['c_route', 'country', 'provider_ratecard'],
        ]
        indexes = [
            PartialIndex(
                fields=['c_route', 'country', 'provider_ratecard'],
                unique=True,
                where='status <> \'disabled\''
            ),
        ]

    def __str__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-routing:route_countryrule_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-routing:route_countryrule_update', args=(self.pk,))


class RegionTypeRule(TimeStampedModel, RuleModel):


    # Relationship Fields
    c_route = models.ForeignKey(RoutingGroup, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pyfb_routing_regiontype_rule'
        ordering = ('region', 'type')
        unique_together = [
            ['c_route', 'region', 'type', 'provider_ratecard'],
        ]
        indexes = [
            PartialIndex(
                fields=['c_route', 'region', 'type', 'provider_ratecard'],
                unique=True,
                where='status <> \'disabled\''
            ),
        ]

    def __str__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-routing:route_regiontyperule_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-routing:route_regiontyperule_update', args=(self.pk,))


class RegionRule(TimeStampedModel, RuleModel):


    # Relationship Fields
    c_route = models.ForeignKey(RoutingGroup, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pyfb_routing_region_rule'
        ordering = ('region',)
        unique_together = [
            ['c_route', 'region', 'provider_ratecard'],
        ]
        indexes = [
            PartialIndex(
                fields=['c_route', 'region', 'provider_ratecard'],
                unique=True,
                where='status <> \'disabled\''
            ),
        ]

    def __str__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-routing:route_regionrule_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-routing:route_regionrule_update', args=(self.pk,))


class DefaultRule(TimeStampedModel, RuleModel):


    # Relationship Fields
    c_route = models.ForeignKey(RoutingGroup, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pyfb_routing_default_rule'
        ordering = ('-pk',)
        unique_together = [
            ['c_route', 'provider_ratecard'],
            # Pour une destination, le route_type doit-etre identique
        ]
        indexes = [
            PartialIndex(
                fields=['c_route', 'provider_ratecard'],
                unique=True,
                where='status <> \'disabled\''
            ),
        ]

    def __str__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-routing:route_defaultrule_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-routing:route_defaultrule_update', args=(self.pk,))
