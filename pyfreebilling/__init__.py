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
from django.contrib import admin
from django import forms
from django.contrib.contenttypes import generic
from yawdadmin import admin_site
from yawdadmin.admin_options import OptionSetAdmin, SiteOption

class SocialOptions(OptionSetAdmin):
	optionset_label = 'socialoptions'
	verbose_name = 'Social Options'

	twitter_id = SiteOption(field=forms.CharField(
		help_text='Twitter Id. This one is required!',
		))

	facebook_id = SiteOption(field=forms.CharField(
		help_text='Url Complet. This one is required!',
		))

	googleplus_id = SiteOption(field=forms.CharField(
		help_text='Google+ Id. This one is required!',
		))

class Coordonnees(OptionSetAdmin):
	optionset_label = 'Address'
	verbose_name = 'Your address'

	address = SiteOption(field=forms.CharField(
		help_text='address. This one is required!',
		))

	address_2 = SiteOption(field=forms.CharField(
		required=False,
		help_text='address_2. This one is optional',
		))

	postal_code = SiteOption(field=forms.CharField(
		help_text='postal_code. This one is required!',
		))

	town = SiteOption(field=forms.CharField(
		help_text='town. This one is required!',
		))

	country = SiteOption(field=forms.CharField(
		help_text='country. This one is required!',
		))
		
	email = SiteOption(field=forms.CharField(
		help_text='email. This one is required!',
		))

	phone = SiteOption(field=forms.CharField(
		required=False,
		help_text='phone. This one is optional',
		))


class CustomOptions(OptionSetAdmin):
    optionset_label = 'custom-options'
    verbose_name = 'Custom Options'

    option_1 = SiteOption(field=forms.CharField(
            widget=forms.Textarea(
                    attrs = {'class' : 'textarea-medium'}
            ),
            required=False,
            help_text='A fancy custom text area option.',
    ))

    option_2 = SiteOption(field=forms.CharField(
            help_text='The second awesome option. This one is required!',
    ))
        
    option_3 = SiteOption(field=forms.BooleanField(
        required=False,
        help_text='Another custom option',
        label='Boolean'
    ))

#register the OptionSetAdmin to the admin site
#almost like we would do for a ModelAdmin
#admin_site.register_options(SocialOptions)
#admin_site.register_options(Coordonnees)
#admin_site.register_options(CustomOptions)