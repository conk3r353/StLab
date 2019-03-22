from django.core.management.base import BaseCommand
from main.models import Shop, Department, Item


class Command(BaseCommand):
    help = 'Clears tables of the models Shop, Department and Item'

    def handle(self, *args, **options):
        Item.objects.all().delete()
        Department.objects.all().delete()
        Shop.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('All data successfully cleared.'))
