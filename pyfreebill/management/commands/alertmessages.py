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
                    #print "balance"
                    qs = Company.objects.filter(customer_enabled=True).exclude(email_alert__isnull=True).exclude(email_alert__exact='')
                    for c in qs:
                        #print "name %s - balance %s - email : %s "% (c.name, c.customer_balance, c.email_alert)
                        send_templated_mail(
                            template_name='balance',
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[c.email_alert],
                            context={
                                'company':c.name,
                                'balance':c.customer_balance,
                                'signature':settings.EMAIL_SIGNATURE
                            },
                        )
                elif var == "lowbalance":
                    print "lowbalance"
                    qs = Company.objects.filter(customer_enabled=True).exclude(email_alert__isnull=True).exclude(email_alert__exact='')
                    for c in qs:
                        """ CREDIT LIMIT ALERT """
                        print "name %s - balance %s - low_credit_alert : %s - low_credit_alert_sent : %s"% (c.name, c.customer_balance, c.low_credit_alert, c.low_credit_alert_sent)
                        # Check alert status and update if necessary
                        if c.low_credit_alert_sent == True and c.customer_balance > c.low_credit_alert:
                            print "balance > low_credit_alert and low_credit_alert_sent is true"
                            # set low_credit_alert to False
                            c.low_credit_alert_sent = False
                            c.save()
                        elif c.low_credit_alert_sent == False and c.customer_balance > c.low_credit_alert:
                            print "balance > low_credit_alert and low_credit_alert_sent is false"
                            # Nothing to do - good
                            pass
                        elif c.low_credit_alert_sent == False and c.customer_balance <= c.low_credit_alert:
                            print "balance < low_credit_alert and low_credit_alert_sent is false"
                            # set low_credit_alert to True
                            c.low_credit_alert_sent = True
                            c.save()
                            # send alert email
                            send_templated_mail(
                                template_name='lowbalance',
                                from_email=settings.EMAIL_HOST_USER,
                                recipient_list=[c.email_alert],
                                context={
                                    'company':c.name,
                                    'balance':c.customer_balance,
                                    'creditalert':c.low_credit_alert,
                                    'signature':settings.EMAIL_SIGNATURE
                                },
                            )
                        """ CREDIT OVER """
                        print "name %s - prepaid : %s - balance %s - credit_limit : %s - account_blocked_alert_sent : %s"% (c.name, c.prepaid, c.customer_balance, c.credit_limit, c.account_blocked_alert_sent)
                        # Check alert status and update if necessary
                        if c.account_blocked_alert_sent == True:
                            if ((c.prepaid == False and c.customer_balance > c.credit_limit) or (c.prepaid == True and c.customer_balance > 0)):
                                print "balance > credit_limit or 0 and account_blocked_alert_sent is true"
                                # set account_blocked_alert to False
                                c.account_blocked_alert_sent = False
                                c.save()
                        elif c.account_blocked_alert_sent == False:
                            if ((c.prepaid == False and c.customer_balance <= c.credit_limit) or (c.prepaid == True and c.customer_balance <= 0)):
                                print "balance < credit_limit or 0 and account_blocked_alert_sent is false"
                                # set account_blocked_alert to True
                                c.account_blocked_alert_sent = True
                                c.save()
                                # send alert email
                                send_templated_mail(
                                    template_name='nobalance',
                                    from_email=settings.EMAIL_HOST_USER,
                                    recipient_list=[c.email_alert],
                                    context={
                                        'company':c.name,
                                        'balance':c.customer_balance,
                                        'signature':settings.EMAIL_SIGNATURE
                                    },
                                )
                elif var == "custom":
                    pass
                else:
                    return

#            except:
#               return CommandError

        self.stdout.write('Successfully alerts ')
