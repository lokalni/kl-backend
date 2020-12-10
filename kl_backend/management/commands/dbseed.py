from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now, timedelta
from model_mommy import mommy

from kl_conferences.models import ServerNode, PreferredServer
from kl_participants.models import Group, Student, Moderator


class Command(BaseCommand):
    help = 'Populate database with sample data'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        if ServerNode.objects.exists():
            return

        # Create django admin user
        adm_user = User.objects.create_superuser('admin', 'admin@admin.admin', 'admin')
        adm_mod = mommy.make(Moderator, user=adm_user, display_name='Admin', access_token='ADMIN')

        s1 = ServerNode.objects.create(
            enabled=True, region="malopolska", display_name='Serwer 1', hostname='abcdef.com', last_heartbeat=now())
        s2 = ServerNode.objects.create(
            enabled=True, region="podkarpackie", display_name='Serwer 2', hostname='ghijkl.com', last_heartbeat=now() - timedelta(seconds=100))
        s4 = ServerNode.objects.create(
            enabled=True, region="lubelskie", display_name='Serwer 3', hostname='mnopqr.com', last_heartbeat=now() - timedelta(seconds=150))
        s5 = ServerNode.objects.create(
            enabled=False, region="malopolska", display_name='Serwer 4', hostname='stuvwx.com', last_heartbeat=now() - timedelta(seconds=250))

        # Add class groups
        g1 = Group.objects.create(display_name='klasa 3A szkola 1')
        g2 = Group.objects.create(display_name='klasa 2C szkola 1')
        g3 = Group.objects.create(display_name='klasa 1B szkola 2')

        # Define preferred servers
        PreferredServer.objects.create(group=g2, server=s1, priority=2)
        PreferredServer.objects.create(group=g2, server=s2, priority=1)

        PreferredServer.objects.create(group=g3, server=s2, priority=2)
        PreferredServer.objects.create(group=g3, server=s1, priority=1)

        # Add teachers
        m1 = mommy.make(Moderator, display_name='Nauczyciel grupa 1 i 2', access_token='NAU1')
        m1.groups.add(g1, g2)

        m2 = mommy.make(Moderator, display_name='Nauczyciel grupa 1 i 3', access_token='NAU2')
        m2.groups.add(g1, g3)

        m3 = mommy.make(Moderator, display_name='Nauczyciel grupa 3', access_token='NAU3')
        m3.groups.add(g3)

        # Add sample student to class groups
        Student.objects.create(display_name='uczen1', group=g1, access_token='UCZEN1')
        Student.objects.create(display_name='uczen2', group=g1, access_token='UCZEN2')

        Student.objects.create(display_name='uczen3', group=g2, access_token='UCZEN3')
        Student.objects.create(display_name='uczen4', group=g2, access_token='UCZEN4')

        Student.objects.create(display_name='uczen5', group=g3, access_token='UCZEN5')
        Student.objects.create(display_name='uczen6', group=g3, access_token='UCZEN6')


