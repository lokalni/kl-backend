from django.core.management.base import BaseCommand, CommandError

from kl_conferences.models import ServerNode
from kl_participants.models import Group, Student, Moderator


class Command(BaseCommand):
    help = 'Populate database with sample data'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        if ServerNode.objects.exists():
            return

        s1 = ServerNode.objects.create(display_name='Serwerek 1', url='dupa.dupa.com/123')
        s2 = ServerNode.objects.create(display_name='Serwerek 2', url='dupa.dupa.com/456')

        # Add class groups
        g1 = Group.objects.create(display_name='klasa 3A szkola 1')
        g2 = Group.objects.create(display_name='klasa 2C szkola 1')
        g3 = Group.objects.create(display_name='klasa 1B szkola 2')

        # Add teachers
        m1 = Moderator.objects.create(display_name='Profesur z pierwszej szkoly')
        m1.groups.add(g1, g2)

        m2 = Moderator.objects.create(display_name='Profesur w 2 szkolach dorabia')
        m2.groups.add(g1, g3)

        m3 = Moderator.objects.create(display_name='Profesur z drugiej szkoly')
        m3.groups.add(g3)

        # Add sample student to class groups
        Student.objects.create(display_name='Seba', group=g1, access_token='SEBA')
        Student.objects.create(display_name='Karyna', group=g1, access_token='KARYNA')

        Student.objects.create(display_name='Brian', group=g2, access_token='BRIAN')
        Student.objects.create(display_name='Nicolette', group=g2, access_token='MAXOSIEM')

        Student.objects.create(display_name='Nadzieja', group=g3, access_token='NADZIEJA')
        Student.objects.create(display_name='Ahmed', group=g3, access_token='AHMED')


