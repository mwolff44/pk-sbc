# -*- coding: utf-8 -*-
from django.urls import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import AutoSlugField

from model_utils.models import TimeStampedModel


class Company(TimeStampedModel):

    # Fields
    name = models.CharField(_(u'name'), max_length=200, unique=True, help_text=_(u"company name - must be unique"))
    slug = AutoSlugField(populate_from='name', blank=True)
    address = models.CharField(_(u'address'), max_length=64, help_text=_(u"address"))
    contact_name = models.CharField(_(u'contact name'), max_length=30, help_text=_(u"contact name"))
    contact_phone = models.CharField(_(u'contact phone'), max_length=30, help_text=_(u"contact phone number"))
#    customer_balance = models.DecimalField(_(u'customer balance'), max_digits=12, decimal_places=6, default=0, help_text=_(u"actual customer balance."))
#    supplier_balance = models.DecimalField(_(u'provider balance'), max_digits=12, decimal_places=6, default=0, help_text=_(u"actual provider balance."))
#    customer_balance_update = models.BooleanField(_(u"customer balance is updated after each call"), default=True)
#    provider_balance_update = models.BooleanField(_(u"provider balance is updated after each call"), default=False)

    class Meta:
        db_table = 'pyfb_company'
        ordering = ('name',)
        verbose_name = _(u'company')
        verbose_name_plural = _(u'companies')

    def __str__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('pyfb-company:pyfb_company_company_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('pyfb-company:pyfb_company_company_update', args=(self.slug,))


class Customer(TimeStampedModel):

    # Fields
    account_number = models.CharField(_(u'account number'), max_length=100)
    credit_limit = models.DecimalField(_(u'credit limit'), max_digits=12, decimal_places=4, default=0, help_text=_(u"Credit limit - Negative value to allow discovery."))
    low_credit_alert = models.DecimalField(_(u'low credit level alert'), max_digits=12, decimal_places=4, default="10", help_text=_(u"Low credit limit alert."))
    max_calls = models.PositiveIntegerField(_(u'max simultaneous calls'), default=1, help_text=_(u"maximum simultaneous calls allowed for this customer account."))
    calls_per_second = models.PositiveIntegerField(_(u'max calls per second'), default=10, help_text=_(u"maximum calls per seconds allowed for this customer account."))
    customer_enabled = models.BooleanField(_(u"customer enabled / disabled"), default=True)
    blocking_credit_limit = models.BooleanField(_(u"block calls if credit limit is reached"), default=True)
    customer_balance = models.DecimalField(_(u'customer balance'), max_digits=12, decimal_places=6, default=0, help_text=_(u"actual customer balance."))
    customer_balance_update = models.BooleanField(_(u"customer balance is updated after each call"), default=True)

    # Relationship Fields
    company = models.OneToOneField(
        'pyfb_company.Company',
        on_delete=models.CASCADE, related_name="customers"
    )

    class Meta:
        db_table = 'pyfb_customer'
        ordering = ('company',)
        verbose_name = _(u'customer')
        verbose_name_plural = _(u'customers')

    def __str__(self):
        return u'%s' % self.company

    def get_absolute_url(self):
        return reverse('pyfb-company:pyfb_company_customer_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-company:pyfb_company_customer_update', args=(self.pk,))

    def colored_name(self):
        if self.customer_enabled == False:
            color = "orange"
        else:
            color = "green"
        return " <span style=color:%s>%s</span>" % (color, self.name)
    colored_name.allow_tags = True


class Provider(TimeStampedModel):

    # Fields
    supplier_enabled = models.BooleanField(_(u"provider enabled / disabled"), default=True)
    supplier_balance = models.DecimalField(_(u'provider balance'), max_digits=12, decimal_places=6, default=0, help_text=_(u"actual provider balance."))
    provider_balance_update = models.BooleanField(_(u"provider balance is updated after each call"), default=False)

    # Relationship Fields
    company = models.OneToOneField(
        'pyfb_company.Company',
        on_delete=models.CASCADE, related_name="providers"
    )

    class Meta:
        db_table = 'pyfb_provider'
        ordering = ('company',)
        verbose_name = _(u'provider')
        verbose_name_plural = _(u'providers')

    def __str__(self):
        return u'%s' % self.company

    def get_absolute_url(self):
        return reverse('pyfb-company:pyfb_company_provider_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-company:pyfb_company_provider_update', args=(self.pk,))

    def colored_name(self):
        if self.supplier_enabled == False:
            color = "orange"
        else:
            color = "green"
        return " <span style=color:%s>%s</span>" % (color, self.name)
    colored_name.allow_tags = True


class CompanyBalanceHistory(TimeStampedModel):

    # Choices
    OPERATION_TYPE_CHOICES = (
        ('customer', _(u"operation on customer account")),
        ('provider', _(u"operation on provider account")),
    )

    # Fields
    amount_debited = models.DecimalField(_(u'amount debited'), max_digits=12, decimal_places=4)
    amount_refund = models.DecimalField(_(u'amount refund'), max_digits=12, decimal_places=4)
    customer_balance = models.DecimalField(_(u'customer balance'), max_digits=12, decimal_places=4, default=0, help_text=_(u"resulting customer balance."))
    supplier_balance = models.DecimalField(_(u'provider balance'), max_digits=12, decimal_places=4, default=0, help_text=_(u"resulting provider balance."))
    operation_type = models.CharField(_(u"operation type"), max_length=10, choices=OPERATION_TYPE_CHOICES, default='customer')
    external_desc = models.CharField(_(u'public description'), max_length=255, blank=True)
    internal_desc = models.CharField(_(u'internal description'), max_length=255, blank=True)

    # Relationship Fields
    company = models.ForeignKey(
        'pyfb_company.Company',
        on_delete=models.CASCADE, related_name="companys", verbose_name=_(u"company")
    )

    class Meta:
        db_table = 'pyfb_company_balance_history'
        ordering = ('company', '-created')
        verbose_name = _(u'company balance history')
        verbose_name_plural = _(u'company balance history')

    def __str__(self):
        return u"%s %s %s %s" % (self.company,
                                 self.amount_debited,
                                 self.amount_refund,
                                 self.operation_type)

    def get_absolute_url(self):
        return reverse('pyfb-company:pyfb_company_companybalancehistory_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-company:pyfb_company_companybalancehistory_update', args=(self.pk,))
