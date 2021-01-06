# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel

from pyfb_company.models import Customer, Provider

from pyfb_endpoint.models import CustomerEndpoint


class Did(TimeStampedModel):
    """
    DID model
    """

    # Fields
    number = models.CharField(_(u'DID number'), max_length=30, db_index=True, unique=True)
    prov_max_channels = models.PositiveIntegerField(_(u'provider channels'), default=0, help_text=_(u"maximum simultaneous calls allowed for this did. 0 means no limit"))
    provider_free = models.BooleanField(_(u'Free from provider'), default=True)
    cust_max_channels = models.PositiveIntegerField(_(u'customer channels'), default=0, null=True, blank=True, help_text=_(u"maximum simultaneous calls allowed for this did. 0 means no limit"))
    customer_free = models.BooleanField(_(u'Free for customer'), default=True)
    insee_code = models.CharField(_(u'Special code for routing urgency numbers'), null=True, blank=True, max_length=10, help_text=_(u"Postal code, INSEE code ... for routing urgency number to the right urgency call center."))
    description = models.CharField(_(u'description'), max_length=30, blank=True)

    # Relationship Fields
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='didprovider', verbose_name=_(u"Provider"), limit_choices_to={'supplier_enabled': True})
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, related_name='didcustomer', verbose_name=_(u"Customer"), null=True, blank=True, limit_choices_to={'customer_enabled': True})


    class Meta:
        db_table = 'pyfb_did'
        ordering = ('number', )
        verbose_name = _(u'DID')
        verbose_name_plural = _(u'DIDs')

    def __str__(self):
        return u"%s (:%s)" % (self.number, self.provider)

    def get_absolute_url(self):
        return reverse('pyfb-did:pyfb_did_did_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-did:pyfb_did_did_update', args=(self.pk,))


class RoutesDid(TimeStampedModel):
    """
    routing plan
    """
    # Choices
    ROUTE_TYPE_CHOICES = (
        ('s', _(u'SIP Trunk')),
        ('e', _(u'External number')),
    )

    # Fields
    order = models.IntegerField(default=1)
    type = models.CharField(_(u'Route type'), max_length=2, choices=ROUTE_TYPE_CHOICES, default='s', help_text=_(u"Routing type : sip trunk (s) orexternal number (e)."))
    number = models.CharField(_(u'destination number'), max_length=30, null=True, blank=True, default='')
    weight = models.PositiveIntegerField(_(u'weight'), default=0)
    description = models.CharField(_(u'description'), max_length=30, blank=True)

    # Relationship Fields
    contract_did = models.ForeignKey(Did, on_delete=models.CASCADE)
    trunk = models.ForeignKey(CustomerEndpoint, null=True, blank=True, on_delete=models.CASCADE)


    class Meta:
        db_table = 'pyfb_did_routes'
        ordering = ('contract_did', )
        unique_together = ('contract_did', 'order')
        verbose_name = _(u'DID route')
        verbose_name_plural = _(u'DID routes')

    def __str__(self):
        return u"%s pos:%s (type:%s / %s %s)" % (self.contract_did,
                                                 self.order,
                                                 self.type,
                                                 self.number,
                                                 self.trunk)

    def get_absolute_url(self):
        return reverse('pyfb-did:pyfb_did_routesdid_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-did:pyfb_did_routesdid_update', args=(self.pk,))
