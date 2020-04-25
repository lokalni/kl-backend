import requests
from django.core.management.base import BaseCommand
from kl_conferences.models import ServerNode

class Command(BaseCommand):
    help = 'Update server nodes in relation to prometheus alerts'

    def add_arguments(self, parser):
        parser.add_argument('prometheus', type=str, help='Prometheus host', required=True)

    def handle(self, *args, **options):
        if ServerNode.objects.exists():
            return

        # Fetch latest alert list from prometheus
        alerts = requests.get("http://{prometheus_host}:9090/api/v1/alerts".format(
            prometheus_host = options['prometheus']
        )).json().get('data', {}).get('alerts', [])

        # Go thru each server and check if it should be enabled or not
        for server in ServerNode.objects.all():
            server.enabled = True
            for alert in alerts:
                if server.hostname in alert['labels']['instance']:
                    server.enabled = False
            server.save()