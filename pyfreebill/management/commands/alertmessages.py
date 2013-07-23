from django.core.management.base import BaseCommand, CommandError
from pyfreebill.models import Company
from templated_email import send_templated_mail
from django.conf import settings

class Command(BaseCommand):
    args = '<date>'
    help = 'Alert messages - balance, balance status - lowbalance, alert low balance - custom '

    def handle(self, *args, **options):
        for var in args:
#            try:

                if var == "balance":
                     print "balance"
                     qs = Company.objects.filter(customer_enabled=True)
                     for c in qs:
                         print "name %s - balance %s - email : %s "% (c.name, c.customer_balance, c.email_alert)
                         send_templated_mail(
                             template_name='welcome',
                             from_email=settings.EMAIL_HOST_USER,
                             recipient_list=[c.email_alert],
                             context={
                                 'username':c.name,
                                 'full_name':c.customer_balance,
                                 'signup_date':c.customer_balance
                             },
                         )
                elif var == "lowbalance":
                     pass
                elif var == "custom":
                    pass
                else:
                    return

#            except:
#               return CommandError

        self.stdout.write('Successfully alerts ')
