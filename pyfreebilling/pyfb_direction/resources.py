# -*- coding: utf-8 -*-
from import_export import resources

from .models import Prefix


class PrefixResource(resources.ModelResource):

    class Meta:
        model = Prefix
        fields = ('prefix')
