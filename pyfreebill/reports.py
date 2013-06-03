from pyfreebill.models import CDR
from django.utils.translation import ugettext_lazy as _
import datetime, qsstats

qs = CDR.objects.all()
qss = qsstats.QuerySetStats(qs, 'start_stamp')
