from django.core.management import BaseCommand

from marketplace_parser.models import Vendor


class Command(BaseCommand):
    # A command must define handle()
    def handle(self, *args, **options):
        Vendor.objects.all().delete()