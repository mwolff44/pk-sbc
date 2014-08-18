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

# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.auth.views import login
from django.shortcuts import get_object_or_404

from braces.views import LoginRequiredMixin

from pyfreebill.models import Company, Person


class HomePageCustView(LoginRequiredMixin, TemplateView):
    template_name = 'customer/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageCustView, self).get_context_data(**kwargs)
        user = getattr(self.request, 'user', None)
        usercompany = get_object_or_404(Person, user=user)
        context['company'] = get_object_or_404(Company, name=usercompany.company)
        # prevoir alert quand solde inferieur a alerte - mettre balance en rouge (danger)
        # integrer dernier flux financier - page historique
        # integrer panneau contact et stats
        # pages recherche cdr - liste cdr
        # integrer money
        # integrer facture
        # integrer prestation
        messages.info(self.request, 'Wellcome')
        return context

class ProfileCustView(LoginRequiredMixin, TemplateView):
    template_name = 'customer/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageCustView, self).get_context_data(**kwargs)
        messages.info(self.request, 'Your profile')
        return context