from import_export import resources, fields
from pyfreebill.models import ProviderRates, CustomerRates, CDR

class CDRResource(resources.ModelResource):
    date = fields.Field(column_name='start_stamp')

    class Meta:
        model = CDR
        exclude = ('country',)
        widgets = {
                'published': {'format': '%d.%m.%Y'},
                }
