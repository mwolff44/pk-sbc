from django.core.management.base import BaseCommand, CommandError
from pyfreebill.models import CDR, dailystats
import qsstats

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'calculate on daily basis stats'

    def handle(self, *args, **options):
        for poll_id in args:
            try:
                poll = Poll.objects.get(pk=int(poll_id))
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.opened = False
            poll.save()

            self.stdout.write('Successfully closed poll "%s"' % poll_id)
