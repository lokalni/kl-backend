from django.contrib.auth.models import User
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

        # Create django admin user
        User.objects.create_superuser('admin', 'admin@ddd.ddd', 'admin')

        s1 = ServerNode.objects.create(display_name='Serwer 1', hostname='abcdef.com')
        s2 = ServerNode.objects.create(display_name='Serwer 2', hostname='ghijkl.com')

        # Add class groups
        g1 = Group.objects.create(display_name='klasa 3A szkola 1')
        g2 = Group.objects.create(display_name='klasa 2C szkola 1')
        g3 = Group.objects.create(display_name='klasa 1B szkola 2')

        # Add teachers
        m1 = Moderator.objects.create(display_name='Nauczyciel grupa 1 i 2', access_token='NAU1')
        m1.groups.add(g1, g2)

        m2 = Moderator.objects.create(display_name='Nauczyciel grupa 1 i 3', access_token='NAU1')
        m2.groups.add(g1, g3)

        m3 = Moderator.objects.create(display_name='Nauczyciel grupa 3', access_token='NAU3')
        m3.groups.add(g3)

        # Add sample student to class groups
        Student.objects.create(display_name='uczen1', group=g1, access_token='UCZEN1')
        Student.objects.create(display_name='uczen2', group=g1, access_token='UCZEN2')

        Student.objects.create(display_name='uczen3', group=g2, access_token='UCZEN3')
        Student.objects.create(display_name='uczen4', group=g2, access_token='UCZEN4')

        Student.objects.create(display_name='uczen5', group=g3, access_token='UCZEN5')
        Student.objects.create(display_name='uczen6', group=g3, access_token='UCZEN6')


