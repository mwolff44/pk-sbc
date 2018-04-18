import unittest
from django.core.urlresolvers import reverse
from django.test import Client
from .models import Destination, Prefix, Carrier, Region, Country, Type
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType


def create_django_contrib_auth_models_user(**kwargs):
    defaults = {}
    defaults["username"] = "username"
    defaults["email"] = "username@tempurl.com"
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_django_contrib_auth_models_group(**kwargs):
    defaults = {}
    defaults["name"] = "group"
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_django_contrib_contenttypes_models_contenttype(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_destination(**kwargs):
    defaults = {}
    defaults["name"] = "name"
    defaults["country_iso2"] = "country_iso2"
    defaults.update(**kwargs)
    if "carrier" not in defaults:
        defaults["carrier"] = create_carrier()
    if "type" not in defaults:
        defaults["type"] = create_type()
    return Destination.objects.create(**defaults)


def create_prefix(**kwargs):
    defaults = {}
    defaults["prefix"] = "prefix"
    defaults.update(**kwargs)
    if "destination" not in defaults:
        defaults["destination"] = create_destination()
    return Prefix.objects.create(**defaults)


def create_carrier(**kwargs):
    defaults = {}
    defaults["name"] = "name"
    defaults.update(**kwargs)
    return Carrier.objects.create(**defaults)


def create_region(**kwargs):
    defaults = {}
    defaults["name"] = "name"
    defaults.update(**kwargs)
    return Region.objects.create(**defaults)


def create_country(**kwargs):
    defaults = {}
    defaults["country_iso2"] = "country_iso2"
    defaults.update(**kwargs)
    if "region" not in defaults:
        defaults["region"] = create_region()
    return Country.objects.create(**defaults)


def create_type(**kwargs):
    defaults = {}
    defaults["name"] = "name"
    defaults.update(**kwargs)
    return Type.objects.create(**defaults)


class DestinationViewTest(unittest.TestCase):
    '''
    Tests for Destination
    '''
    def setUp(self):
        self.client = Client()

    def test_list_destination(self):
        url = reverse('direction_destination_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_destination(self):
        url = reverse('direction_destination_create')
        data = {
            "name": "name",
            "country_iso2": "country_iso2",
            "carrier": create_carrier().pk,
            "type": create_type().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_destination(self):
        destination = create_destination()
        url = reverse('direction_destination_detail', args=[destination.slug,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_destination(self):
        destination = create_destination()
        data = {
            "name": "name",
            "country_iso2": "country_iso2",
            "carrier": create_carrier().pk,
            "type": create_type().pk,
        }
        url = reverse('direction_destination_update', args=[destination.slug,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class PrefixViewTest(unittest.TestCase):
    '''
    Tests for Prefix
    '''
    def setUp(self):
        self.client = Client()

    def test_list_prefix(self):
        url = reverse('direction_prefix_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_prefix(self):
        url = reverse('direction_prefix_create')
        data = {
            "prefix": "prefix",
            "destination": create_destination().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_prefix(self):
        prefix = create_prefix()
        url = reverse('direction_prefix_detail', args=[prefix.slug,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_prefix(self):
        prefix = create_prefix()
        data = {
            "prefix": "prefix",
            "destination": create_destination().pk,
        }
        url = reverse('direction_prefix_update', args=[prefix.slug,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class CarrierViewTest(unittest.TestCase):
    '''
    Tests for Carrier
    '''
    def setUp(self):
        self.client = Client()

    def test_list_carrier(self):
        url = reverse('direction_carrier_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_carrier(self):
        url = reverse('direction_carrier_create')
        data = {
            "name": "name",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_carrier(self):
        carrier = create_carrier()
        url = reverse('direction_carrier_detail', args=[carrier.slug,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_carrier(self):
        carrier = create_carrier()
        data = {
            "name": "name",
        }
        url = reverse('direction_carrier_update', args=[carrier.slug,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class RegionViewTest(unittest.TestCase):
    '''
    Tests for Region
    '''
    def setUp(self):
        self.client = Client()

    def test_list_region(self):
        url = reverse('direction_region_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_region(self):
        url = reverse('direction_region_create')
        data = {
            "name": "name",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_region(self):
        region = create_region()
        url = reverse('direction_region_detail', args=[region.slug,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_region(self):
        region = create_region()
        data = {
            "name": "name",
        }
        url = reverse('direction_region_update', args=[region.slug,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class CountryViewTest(unittest.TestCase):
    '''
    Tests for Country
    '''
    def setUp(self):
        self.client = Client()

    def test_list_country(self):
        url = reverse('direction_country_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_country(self):
        url = reverse('direction_country_create')
        data = {
            "country_iso2": "country_iso2",
            "region": create_region().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_country(self):
        country = create_country()
        url = reverse('direction_country_detail', args=[country.pk,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_country(self):
        country = create_country()
        data = {
            "country_iso2": "country_iso2",
            "region": create_region().pk,
        }
        url = reverse('direction_country_update', args=[country.pk,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class TypeViewTest(unittest.TestCase):
    '''
    Tests for Type
    '''
    def setUp(self):
        self.client = Client()

    def test_list_type(self):
        url = reverse('direction_type_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_type(self):
        url = reverse('direction_type_create')
        data = {
            "name": "name",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_type(self):
        type = create_type()
        url = reverse('direction_type_detail', args=[type.slug,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_type(self):
        type = create_type()
        data = {
            "name": "name",
        }
        url = reverse('direction_type_update', args=[type.slug,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
