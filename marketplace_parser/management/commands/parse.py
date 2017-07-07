from django.core.management import BaseCommand

from marketplace_parser.parser import parse


class Command(BaseCommand):
    # A command must define handle()
    def handle(self, *args, **options):
        parse()