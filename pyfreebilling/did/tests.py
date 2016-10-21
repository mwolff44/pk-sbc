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


from django.test import TestCase
from django.test import Client


from pyfreebill.models import Company

from did.models import Did


class DidViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_url(self):
        urls = [{'url': '/extranet/did/add',
                 'template': 'did/did.html',
                 'status': 200},
                {'url': '/extranet/did',
                 'status': 200}]
        for elem in urls:
            response = self.client.get(elem['url'])
            self.assertEqual(response.status_code, elem['status'])
            response = self.client.get(elem['url'], follow=True)
            self.assertEqual(response.template.name, elem['template'])


class test_Did(TestCase):
    def test_create_provider(self):
        """
        We need a provider for testing did
        """
        provider1 = Company(name="Celea")
        provider1.save()
        provider = Company.objects.get(name="Celea")
        self.assertEqual(provider.name, "Celea")

    def test_create_did(self):
        """
        creation of a new did entry
        """
        self.test_create_provider()
        provider = Company.objects.get(name="Celea")
        did = Did(number='33100110011',
                  provider=provider,
                  max_channels='10',
                  description="did created by MW")
        did.save()
        did = Did.objects.get(number='33100110011')
        self.assertEqual(did.description, u'did created by MW')
