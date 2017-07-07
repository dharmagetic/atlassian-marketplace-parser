from django.core.management import BaseCommand

from marketplace_parser.exporter import export_to_csv


class Command(BaseCommand):
    def handle(self, *args, **options):
        export_to_csv()