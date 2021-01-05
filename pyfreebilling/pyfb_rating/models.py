# -*- coding: utf-8 -*-

from django.core.validators import MaxValueValidator
from django.urls import reverse
from django.db import models as models
from django.db.models import *
from django.conf import settings
from django.contrib.postgres.fields import DateTimeRangeField
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django_extensions.db import fields as extension_fields
from django_extensions.db.fields import AutoSlugField

from model_utils.models import StatusModel, TimeStampedModel
from model_utils import Choices

from partial_index import PartialIndex

from pyfb_company.models import Customer, Provider

from pyfb_direction.models import Country, Destination, Region, Type


# Caller Number List management
class CallerNumList(TimeStampedModel):

    # Choices
    CALLERID_FILTER_CHOICES = (
        ('1', _(u"No filter")),
        ('2', _(u"Prefix authorized")),
        ('3', _(u"Prefix prohibited")),
    )

    # Fields
    name = models.CharField(max_length=128, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    callerid_filter = models.CharField(_(u"CallerID Prefix filter"), max_length=2, choices=CALLERID_FILTER_CHOICES, default='1')

    # Relationship Fields
    destination = models.ManyToManyField(Destination, verbose_name=_(u"destination list"))

    class Meta:
        db_table = 'pyfb_rating_callernum_list'
        ordering = ('-name',)

    def __str__(self):
        return u'%s' % self.slug

    def __str__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('pyfb-rating:pyfb_rating_callernumlist_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('pyfb-rating:pyfb_rating_callernumlist_update', args=(self.slug,))


# Ratecard management
def default_time():
    return timezone.now() + timezone.timedelta(days=3650)


class RatecardModel(models.Model):

    # Fields
    description = models.TextField(_(u'description'), blank=True)
    # To be implemented later, for the time beiing, we will use two separated fields
    # date_validity = DateTimeRangeField()
    date_start = models.DateTimeField(default=timezone.now)
    date_end = models.DateTimeField(default=default_time)

    # Relationship Fields
    callerid_list = models.ForeignKey(CallerNumList,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class CustomerRatecard(StatusModel, TimeStampedModel, RatecardModel):

    # choices
    RCTYPE_CHOICES = (
        ('pstn', _(u"Outbound calls")),
        ('did', _(u"DID - Inbound calls")),
        ('pstn2did', _(u"Outbound calls to internal DID")),
        ('emergency', _(u"Emergency calls"))
    )
    STATUS = Choices(
        ('enabled', _(u"Enabled")),
        ('disabled', _(u"Disabled")),
    )

    # Fields
    name = models.CharField(_(u"ratecard name"), max_length=128, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    rc_type = models.CharField(_(u"type of ratecards"), max_length=10, choices=RCTYPE_CHOICES, default='pstn', help_text=_(u"Select the right ratecard regarding the type of calls. Default is PSTN"))

    class Meta:
        db_table = 'pyfb_rating_c_ratecard'
        ordering = ('name',)
        indexes = [
            PartialIndex(fields=['id', 'rc_type'], unique=False, where_postgresql='status = \'enabled\''),
            PartialIndex(fields=['id', 'rc_type'], unique=False, where='status = \'enabled\' AND rc_type = \'PSTN\''),
            PartialIndex(fields=['id', 'rc_type'], unique=False, where='status = \'enabled\' AND rc_type = \'DIDIN\''),
            PartialIndex(fields=['id', 'rc_type'], unique=False, where='status = \'enabled\' AND rc_type = \'DIDOUT\''),
            PartialIndex(fields=['id', 'rc_type'], unique=False, where='status = \'enabled\' AND rc_type = \'EMERGENCY\''),
        ]

    def __str__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('pyfb-rating:pyfb_rating_customerratecard_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('pyfb-rating:pyfb_rating_customerratecard_update', args=(self.slug,))


class CustomerRcAllocation(TimeStampedModel):
    """ Customer rates Cards Model """

    # choices
    DEFAULT_PRIORITY_CHOICES = (
        (1, _(u'1')),
        (2, _(u'2')),
        (3, _(u'3')),
        (4, _(u'4')),
        (5, _(u'5')),
        (6, _(u'6')),
        (7, _(u'7')),
    )

    # Fields
    tech_prefix = models.CharField(_(u"technical prefix"), blank=True, default='', max_length=7)
    priority = models.IntegerField(_(u'priority'), choices=DEFAULT_PRIORITY_CHOICES, help_text=_(u"Priority order, 1 is the higher priority and 3 the lower one. Correct values are : 1 to 7 !."))
    discount = models.DecimalField(_(u'discount'), max_digits=5, decimal_places=2, default=0, help_text=_(u"ratecard discount. For 10% discount, enter 10 !"))
    allow_negative_margin = models.BooleanField(_(u"Allow calls with negative margin"), default=False)
    description = models.CharField(_(u'Comment'), max_length=30, blank=True)

    # Relationship Fields
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name=_(u"customer")
    )
    ratecard = models.ForeignKey(
        CustomerRatecard,
        on_delete=models.CASCADE,
        related_name="customerratecards",
        verbose_name=_(u"ratecard")
    )

    class Meta:
        db_table = 'pyfb_rating_cr_allocation'
        ordering = ('customer', 'priority', 'ratecard')
        verbose_name = _(u'Customer Ratecard Allocation')
        verbose_name_plural = _(u'Customer ratecard Allocations')

    def __str__(self):
        return u"%s - %s - Priority: %s Desc: %s" % (self.customer, self.ratecard,
                                                self.priority,
                                                self.description)

    def get_absolute_url(self):
        return reverse('pyfb-rating:pyfb_rating_customerratecards_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-rating:pyfb_rating_customerratecards_update', args=(self.pk,))


class ProviderRatecard(StatusModel, TimeStampedModel, RatecardModel):

    # choices
    RCTYPE_CHOICES = (
        ('pstn', _(u"Outbound calls")),
        ('did', _(u"DID - Inbound calls")),
        ('pstn2did', _(u"Outbound calls to internal DID")),
        ('emergency', _(u"Emergency calls"))
    )
    STATUS = Choices(
        ('enabled', _(u"Enabled")),
        ('disabled', _(u"Disabled")),
    )

    # Fields
    name = models.CharField(_(u"ratecard name"), max_length=128, unique=True)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    rc_type = models.CharField(_(u"type of ratecards"), max_length=10, choices=RCTYPE_CHOICES, default='pstn', help_text=_(u"Select the right ratecard regarding the type of calls. Default is PSTN"))
    provider_prefix = models.CharField(_(u'tech prefix'), max_length=10, default='', blank=True)
    estimated_quality = models.PositiveSmallIntegerField(_(u'quality'), validators=[MaxValueValidator(10)], default='10', help_text=_(u"Estimated quality. Number between 0 to 10"))

    # Relationship Fields
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE, related_name="providers", verbose_name=_(u"Provider")
    )

    class Meta:
        db_table = 'pyfb_rating_p_ratecard'
        ordering = ('provider', 'name',)
        indexes = [
            PartialIndex(fields=['id', 'rc_type'], unique=False, where_postgresql='status = \'enabled\''),
            PartialIndex(fields=['id', 'rc_type'], unique=False, where='status = \'enabled\' AND rc_type = \'PSTN\''),
            PartialIndex(fields=['id', 'rc_type'], unique=False, where='status = \'enabled\' AND rc_type = \'DIDIN\''),
            PartialIndex(fields=['id', 'rc_type'], unique=False, where='status = \'enabled\' AND rc_type = \'DIDOUT\''),
            PartialIndex(fields=['id', 'rc_type'], unique=False, where='status = \'enabled\' AND rc_type = \'EMERGENCY\''),
        ]

    def __str__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('pyfb-rating:pyfb_rating_providerratecard_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('pyfb-rating:pyfb_rating_providerratecard_update', args=(self.slug,))


# Rates management
class RateModel(models.Model):

    # choices
    STATUS_CHOICES = Choices(
        ('enabled', _(u"Enabled")),
        ('enabled_negmargin', _(u"Enabled allowing negative margin")),
        ('disabled', _(u"Disabled")),
        ('blocked', _(u"Blocked")),
    )

    # Fields
    r_rate = models.DecimalField(_(u'sell rate'), max_digits=11, decimal_places=5, help_text=_(u"rate per minute"))
    r_block_min_duration = models.PositiveSmallIntegerField(_(u'Increment'), default=1)
    r_minimal_time = models.PositiveSmallIntegerField(_(u'Minimal time'), default=0, help_text=_(u"minimal time to be billed in seconds"))
    r_init_block = models.DecimalField(_(u'Connection fee'), max_digits=11, decimal_places=5, default=0)
    status = models.CharField(_(u"Status"), max_length=20, default=STATUS_CHOICES.enabled, choices=STATUS_CHOICES, help_text=_(u"State of the rate : enabled / blocked - calls to this destination are blocked / disabled"))
    # To be implemented later, if someone needs this feature
    # date_validity = DateTimeRangeField()

    class Meta:
        abstract = True


class CustomerPrefixRate(TimeStampedModel, RateModel):

    # Fields
    prefix = models.CharField(_(u'numeric prefix'), max_length=30, db_index=True)
    destnum_length = models.PositiveSmallIntegerField(_(u'Destination number length'), default=0, help_text=_(u"If value > 0, then destination number must match tsi length"))

    # Relationship Fields
    c_ratecard = models.ForeignKey(CustomerRatecard, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pyfb_rating_c_prefix_rate'
        ordering = ('c_ratecard',)
        unique_together = [
            ['c_ratecard', 'prefix', 'destnum_length'],
        ]
        indexes = [
            PartialIndex(
                fields=['c_ratecard', 'prefix', 'destnum_length'],
                unique=True,
                where='status <> \'disabled\''
            ),
        ]

    def __str__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-rating:pyfb_rating_customerprefixrate_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-rating:pyfb_rating_customerprefixrate_update', args=(self.pk,))


class ProviderPrefixRate(TimeStampedModel, RateModel):

    # Fields
    prefix = models.CharField(_(u'numeric prefix'), max_length=30, db_index=True)
    destnum_length = models.PositiveSmallIntegerField(_(u'Destination number length'), default=0, help_text=_(u"If value > 0, then destination number must match tsi length"))

    # Relationship Fields
    p_ratecard = models.ForeignKey(ProviderRatecard, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pyfb_rating_p_prefix_rate'
        ordering = ('p_ratecard',)
        unique_together = [
            ['p_ratecard', 'prefix', 'destnum_length'],
        ]
        indexes = [
            PartialIndex(
                fields=['p_ratecard', 'prefix', 'destnum_length'],
                unique=True,
                where='status <> \'disabled\''
            ),
        ]

    def __str__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-rating:pyfb_rating_providerprefixrate_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-rating:pyfb_rating_providerprefixrate_update', args=(self.pk,))


class CustomerDestinationRate(TimeStampedModel, RateModel):


    # Relationship Fields
    c_ratecard = models.ForeignKey(CustomerRatecard, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pyfb_rating_c_destination_rate'
        ordering = ('c_ratecard',)
        unique_together = [
            ['c_ratecard', 'destination'],
        ]
        indexes = [
            PartialIndex(
                fields=['c_ratecard', 'destination'],
                unique=True,
                where='status <> \'disabled\''
            ),
        ]

    def __str__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-rating:pyfb_rating_customerdestinationrate_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-rating:pyfb_rating_customerdestinationrate_update', args=(self.pk,))


class ProviderDestinationRate(TimeStampedModel, RateModel):


    # Relationship Fields
    p_ratecard = models.ForeignKey(ProviderRatecard, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pyfb_rating_p_destination_rate'
        ordering = ('p_ratecard',)
        unique_together = [
            ['p_ratecard', 'destination'],
        ]
        indexes = [
            PartialIndex(
                fields=['p_ratecard', 'destination'],
                unique=True,
                where='status <> \'disabled\''
            ),
        ]

    def __str__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-rating:pyfb_rating_providerdestinationrate_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-rating:pyfb_rating_providerdestinationrate_update', args=(self.pk,))


class CustomerCountryTypeRate(TimeStampedModel, RateModel):


    # Relationship Fields
    c_ratecard = models.ForeignKey(CustomerRatecard, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pyfb_rating_c_countrytype_rate'
        ordering = ('c_ratecard',)
        unique_together = [
            ['c_ratecard', 'country', 'type'],
        ]
        indexes = [
            PartialIndex(
                fields=['c_ratecard', 'country', 'type'],
                unique=True,
                where='status <> \'disabled\''
            ),
        ]

    def __str__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-rating:pyfb_rating_customercountrytyperate_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-rating:pyfb_rating_customercountrytyperate_update', args=(self.pk,))


class ProviderCountryTypeRate(TimeStampedModel, RateModel):


    # Relationship Fields
    p_ratecard = models.ForeignKey(ProviderRatecard, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pyfb_rating_p_countrytype_rate'
        ordering = ('p_ratecard',)
        unique_together = [
            ['p_ratecard', 'country', 'type'],
        ]
        indexes = [
            PartialIndex(
                fields=['p_ratecard', 'country', 'type'],
                unique=True,
                where='status <> \'disabled\''
            ),
        ]

    def __str__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-rating:pyfb_rating_providercountrytyperate_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-rating:pyfb_rating_providercountrytyperate_update', args=(self.pk,))


class CustomerCountryRate(TimeStampedModel, RateModel):


    # Relationship Fields
    c_ratecard = models.ForeignKey(CustomerRatecard, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pyfb_rating_c_country_rate'
        ordering = ('c_ratecard',)
        unique_together = [
            ['c_ratecard', 'country'],
        ]
        indexes = [
            PartialIndex(
                fields=['c_ratecard', 'country'],
                unique=True,
                where='status <> \'disabled\''
            ),
        ]

    def __str__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-rating:pyfb_rating_customercountryrate_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-rating:pyfb_rating_customercountryrate_update', args=(self.pk,))


class ProviderCountryRate(TimeStampedModel, RateModel):


    # Relationship Fields
    p_ratecard = models.ForeignKey(ProviderRatecard, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pyfb_rating_p_country_rate'
        ordering = ('p_ratecard',)
        unique_together = [
            ['p_ratecard', 'country'],
        ]
        indexes = [
            PartialIndex(
                fields=['p_ratecard', 'country'],
                unique=True,
                where='status <> \'disabled\''
            ),
        ]

    def __str__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-rating:pyfb_rating_providercountryrate_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-rating:pyfb_rating_providercountryrate_update', args=(self.pk,))


class CustomerRegionTypeRate(TimeStampedModel, RateModel):


    # Relationship Fields
    c_ratecard = models.ForeignKey(CustomerRatecard, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pyfb_rating_c_regiontype_rate'
        ordering = ('c_ratecard',)
        unique_together = [
            ['c_ratecard', 'region', 'type'],
        ]
        indexes = [
            PartialIndex(
                fields=['c_ratecard', 'region', 'type'],
                unique=True,
                where='status <> \'disabled\''
            ),
        ]

    def __str__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-rating:pyfb_rating_customerregiontyperate_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-rating:pyfb_rating_customerregiontyperate_update', args=(self.pk,))


class ProviderRegionTypeRate(TimeStampedModel, RateModel):


    # Relationship Fields
    p_ratecard = models.ForeignKey(ProviderRatecard, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pyfb_rating_p_regiontype_rate'
        ordering = ('p_ratecard',)
        unique_together = [
            ['p_ratecard', 'region', 'type'],
        ]
        indexes = [
            PartialIndex(
                fields=['p_ratecard', 'region', 'type'],
                unique=True,
                where='status <> \'disabled\''
            ),
        ]

    def __str__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-rating:pyfb_rating_providerregiontyperate_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-rating:pyfb_rating_providerregiontyperate_update', args=(self.pk,))


class CustomerRegionRate(TimeStampedModel, RateModel):


    # Relationship Fields
    c_ratecard = models.ForeignKey(CustomerRatecard, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pyfb_rating_c_region_rate'
        ordering = ('c_ratecard',)
        unique_together = [
            ['c_ratecard', 'region'],
        ]
        indexes = [
            PartialIndex(
                fields=['c_ratecard', 'region'],
                unique=True,
                where='status <> \'disabled\''
            ),
        ]

    def __str__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-rating:pyfb_rating_customerregionrate_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-rating:pyfb_rating_customerregionrate_update', args=(self.pk,))


class ProviderRegionRate(TimeStampedModel, RateModel):


    # Relationship Fields
    p_ratecard = models.ForeignKey(ProviderRatecard, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pyfb_rating_p_region_rate'
        ordering = ('p_ratecard',)
        unique_together = [
            ['p_ratecard', 'region'],
        ]
        indexes = [
            PartialIndex(
                fields=['p_ratecard', 'region'],
                unique=True,
                where='status <> \'disabled\''
            ),
        ]

    def __str__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-rating:pyfb_rating_providerregionrate_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-rating:pyfb_rating_providerregionrate_update', args=(self.pk,))


class CustomerDefaultRate(TimeStampedModel, RateModel):


    # Relationship Fields
    c_ratecard = models.ForeignKey(CustomerRatecard, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pyfb_rating_c_default_rate'
        ordering = ('c_ratecard',)
        indexes = [
            models.Index(fields=['c_ratecard']),
            PartialIndex(
                fields=['c_ratecard'],
                unique=True,
                where='status <> \'disabled\''
            ),
        ]

    def __str__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-rating:pyfb_rating_customerdefaultrate_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-rating:pyfb_rating_customerdefaultrate_update', args=(self.pk,))


class ProviderDefaultRate(TimeStampedModel, RateModel):


    # Relationship Fields
    p_ratecard = models.ForeignKey(ProviderRatecard, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pyfb_rating_p_default_rate'
        ordering = ('p_ratecard',)
        indexes = [
            models.Index(fields=['p_ratecard']),
            PartialIndex(
                fields=['p_ratecard'],
                unique=True,
                where='status <> \'disabled\''
            ),
        ]

    def __str__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('pyfb-rating:pyfb_rating_providerdefaultrate_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-rating:pyfb_rating_providerdefaultrate_update', args=(self.pk,))
