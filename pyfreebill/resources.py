from import_export import fields
from pyfreebill.models import rates, CDR

class RatesResource(resources.ModelResource):

    class Meta:
        model = Rates

class CDRResource(resources.ModelResource):

    class Meta:
        model = CDR
