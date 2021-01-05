# -*- coding: utf-8 -*-
from django.urls import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel


class NormalizationGrp(TimeStampedModel):
    """Normalization group table"""
    name = models.CharField(
        _(u'Rule Group name'),
        max_length=30)
    description = models.TextField(
        _(u'description'),
        blank=True)

    class Meta:
        db_table = 'pyfb_normalization_grp'
        ordering = ('name',)
        verbose_name = _(u'Normalization Group')
        verbose_name_plural = _(u'Normalization Groups')

    def __str__(self):
        return u'%s' % self.name

    def __unicode__(self):
        return u"%s" % (self.name)

    def get_absolute_url(self):
        return reverse('pyfb-normalization:pyfb_normalization_normalizationgrp_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-normalization:pyfb_normalization_normalizationgrp_update', args=(self.pk,))


class NormalizationRule(TimeStampedModel):
    """ Normalization rules table """
    name = models.CharField(
        _(u'rule title'),
        max_length=30)
    DEFAULT_MATCH = (
        (0, _(u'Equal')),
        (1, _(u'Regex')),
    )
    match_op = models.IntegerField(
        _(u'Type of match (equal or regex)'),
        choices=DEFAULT_MATCH,
        default=1)
    match_exp = models.CharField(
        _(u"match expression"),
        blank=True,
        default='',
        max_length=64,
        help_text=_(u"""Example : ^(33)[0-9].*"""))
    match_len = models.IntegerField(
        _(u'match length'),
        default=0)
    subst_exp = models.CharField(
        _(u"substitution expression"),
        blank=True,
        default='',
        max_length=64,
        help_text=_(u"""Example : ^(33)([0-9].*)"""))
    repl_exp = models.CharField(
        _(u"replacement expression"),
        blank=True,
        default='',
        max_length=64,
        help_text=_(u"""Example : 0033\1"""))
    DEFAULT_CALL = (
        ("", _(u'N/A')),
    )
    attrs = models.CharField(
        _(u"attributes"),
        blank=True,
        choices=DEFAULT_CALL,
        default='',
        max_length=64,
        help_text=_(u"""Rule to map specific route -
            Default set to nothing : N/A - not used"""))
    description = models.TextField(
        _(u'description'),
        blank=True)

    class Meta:
        db_table = 'pyfb_normalization_rule'
        ordering = ('name', 'match_exp')
        verbose_name = _(u'Normalization Rule')
        verbose_name_plural = _(u'Normalization Rules')

    def __str__(self):
        return u"%s (%s:%s)" % (self.name, self.match_op, self.match_exp)

    def __unicode__(self):
        return u"%s (%s:%s)" % (self.name, self.match_op, self.match_exp)

    def get_absolute_url(self):
        return reverse('pyfb-normalization:pyfb_normalization_normalizationrule_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-normalization:pyfb_normalization_normalizationrule_update', args=(self.pk,))


class NormalizationRuleGrp(TimeStampedModel):
    """ Normalization rules group table """
    pr = models.IntegerField(
        _(u'priority'),
        help_text=_(u"""Rule order"""))
    description = models.TextField(
        _(u'description'),
        blank=True)

    # Relationship Fields
    dpid = models.ForeignKey(
        'pyfb_normalization.NormalizationGrp',
        on_delete=models.PROTECT,
        related_name="normalizationgrps",
        verbose_name=_(u"Normalization Group")
    )
    rule = models.ForeignKey(
        'pyfb_normalization.NormalizationRule',
        on_delete=models.PROTECT,
        related_name="normalizationrules",
        verbose_name=_(u"Normalization Rule")
    )

    class Meta:
        db_table = 'pyfb_normalization_rule_grp'
        ordering = ('dpid', 'pr')
        unique_together = (("dpid", "pr"),)
        verbose_name = _(u'Normalization Rule-Group')
        verbose_name_plural = _(u'Normalization Rules-Groups')

    def __str__(self):
        return u"%s - Priority: %s Rule: %s" % (self.dpid,
                                                self.pr,
                                                self.rule)

    def __unicode__(self):
        return u"%s - Priority: %s Rule: %s" % (self.dpid,
                                                self.pr,
                                                self.rule)

    def get_absolute_url(self):
        return reverse('pyfb-normalization:pyfb_normalization_normalizationrulegrp_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-normalization:pyfb_normalization_normalizationrulegrp_update', args=(self.pk,))


class CallMappingRule(TimeStampedModel):
    """ Normalization call mapping rules table """
    name = models.CharField(
        _(u'rule title'),
        max_length=30)
    dpid = models.IntegerField(
        _(u'Dialplan id'),
        default=0,
        help_text=_(u"""Need to be 0, instead of the rule
            will not be used"""))
    pr = models.IntegerField(
        _(u'Priority rule'),
        unique=True,
        help_text=_(u"""Priority of rule"""))

    DEFAULT_MATCH = (
        (0, _(u'Equal')),
        (1, _(u'Regex')),
    )
    match_op = models.IntegerField(
        _(u'Type of match (equal or regex)'),
        choices=DEFAULT_MATCH,
        default=1)
    match_exp = models.CharField(
        _(u"match expression"),
        blank=True,
        default='',
        max_length=64,
        help_text=_(u"""Example : ^(33)[0-9].*"""))
    match_len = models.IntegerField(
        _(u'match length'),
        default=0)
    subst_exp = models.CharField(
        _(u"subst prefix"),
        blank=True,
        default='',
        max_length=64,
        help_text=_(u"""Example : ^(33)([0-9].*)"""))
    repl_exp = models.CharField(
        _(u"replacement prefix"),
        blank=True,
        default='',
        max_length=64,
        help_text=_(u"""Example : 0033\1"""))
    DEFAULT_CALL = (
        ("", _(u'N/A')),
        ("PSTN", _(u'PSTN')),
        ("EMERGENCY", _(u'EMERGENCY NUMBER')),
        ("OWN", _(u'OWN NUMBERS')),
        ("SPEEDDIAL", _(u'SPEED DIAL')),
        ("DROP", _(u'DROP NUMBERS')),
    )
    attrs = models.CharField(
        _(u"attributes"),
        blank=True,
        choices=DEFAULT_CALL,
        default='',
        max_length=64,
        help_text=_(u"""Rule to map specific route -
            Default set to nothing : N/A"""))
    description = models.TextField(
        _(u'description'),
        blank=True)

    class Meta:
        db_table = 'pyfb_call_mapping_rule'
        ordering = ('pr',)
        unique_together = (("dpid", "pr"),)
        verbose_name = _(u'Call Mapping Rule')
        verbose_name_plural = _(u'Call Mapping Rules')

    def __str__(self):
        return u"%s- %s %s (%s/%s) %s" % (
            self.id,
            self.name,
            self.pr,
            self.match_op,
            self.match_exp,
            self.attrs)

    def __unicode__(self):
        return u"%s- %s %s (%s/%s) %s" % (
            self.id,
            self.name,
            self.pr,
            self.match_op,
            self.match_exp,
            self.attrs)

    def get_absolute_url(self):
        return reverse('pyfb-normalization:pyfb_normalization_callmappingrule_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-normalization:pyfb_normalization_callmappingrule_update', args=(self.pk,))
