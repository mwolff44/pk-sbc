import django_tables2 as tables
from pyfreebill.models import CDR

class CDRTable(tables.Table):
    days = tables.Column()
    number_cdr = tables.Column()    
    class Meta:
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
