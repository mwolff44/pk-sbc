from django.core.management.base import BaseCommand, CommandError
from pyfreebill.models import Company

class Command(BaseCommand):
    args = '<date>'
    help = 'Alert messages - balance, balance status - lowbalance, alert low balance - custom '

    def handle(self, *args, **options):
        for var in args:
            try:

                if var == "balance":
                     pass
                elif var == "lowbalance":
                     pass
                elif var == "custom":
                    pass
                else:
                    return

            except:
                raise CommandError('alert does not exist')

            self.stdout.write('Successfully alerts ')
