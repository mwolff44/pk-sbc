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

from django.db import models
from django.utils.translation import ugettext_lazy as _


class NormalizationGroup(models.Model):
    """NormalizationRuleGroup table"""
    name = models.CharField(
        _(u'Rule Group name'),
        max_length=30)
    description = models.TextField(
        _(u'description'),
        blank=True)
    date_added = models.DateTimeField(
        _(u'date added'),
        auto_now_add=True)
    date_modified = models.DateTimeField(
        _(u'date modified'),
        auto_now=True)

    class Meta:
        db_table = 'normalization_grp'
        app_label = 'normalizationrule'
        ordering = ('name',)
        verbose_name = _(u'Normalization Group')
        verbose_name_plural = _(u'Normalization Groups')

    def __unicode__(self):
        return u"%s" % (self.name)


class NormalizationRule(models.Model):
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
    date_added = models.DateTimeField(
        _(u'date added'),
        auto_now_add=True)
    date_modified = models.DateTimeField(
        _(u'date modified'),
        auto_now=True)

    class Meta:
        db_table = 'normalization_rule'
        app_label = 'normalizationrule'
        ordering = ('name', 'match_exp')
        verbose_name = _(u'Normalization Rule')
        verbose_name_plural = _(u'Normalization Rules')

    def __unicode__(self):
        return u"%s (%s:%s)" % (self.name, self.match_op, self.match_exp)


class NormalizationRuleGroup(models.Model):
    """ Customer rates Cards Model """
    dpid = models.ForeignKey(
        NormalizationGroup,
        verbose_name=_(u"Normalization Group"))
    pr = models.IntegerField(
        _(u'priority'),
        help_text=_(u"""Rule order"""))
    rule = models.ForeignKey(
        NormalizationRule,
        verbose_name=_(u"Normalization Rule"))
    description = models.TextField(
        _(u'description'),
        blank=True)
    date_added = models.DateTimeField(
        _(u'date added'),
        auto_now_add=True)
    date_modified = models.DateTimeField(
        _(u'date modified'),
        auto_now=True)

    class Meta:
        db_table = 'normalization_rule_grp'
        app_label = 'normalizationrule'
        ordering = ('dpid', 'pr')
        unique_together = (("dpid", "pr"),)
        verbose_name = _(u'Normalization Rule-Group')
        verbose_name_plural = _(u'Normalization Rules-Groups')

    def __unicode__(self):
        return u"%s - Priority: %s Rule: %s" % (self.dpid,
                                                self.pr,
                                                self.rule)


class CallMappingRule(models.Model):
    """ Normalization rules table """
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
    date_added = models.DateTimeField(
        _(u'date added'),
        auto_now_add=True)
    date_modified = models.DateTimeField(
        _(u'date modified'),
        auto_now=True)

    class Meta:
        db_table = 'call_mapping_rule'
        app_label = 'normalizationrule'
        ordering = ('pr',)
        unique_together = (("dpid", "pr"),)
        verbose_name = _(u'Call Mapping Rule')
        verbose_name_plural = _(u'Call Mapping Rules')

    def __unicode__(self):
        return u"%s %s (%s/%s) %s" % (
            self.name,
            self.pr,
            self.match_op,
            self.match_exp,
            self.attrs)
