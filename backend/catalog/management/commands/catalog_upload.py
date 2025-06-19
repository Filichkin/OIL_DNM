from django.core.management.base import BaseCommand
from django.db import IntegrityError

from oil_dnm import settings
from catalog.models import Catalog
from .utils import excel_preprocess


class Command(BaseCommand):
    help = 'Import data from exel file into Catalog model in database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Path to file')

    def handle(self, *args, **options):
        success_count = 0
        print('Loading data...')
        df = excel_preprocess(f'{settings.BASE_DIR}/data/PriceOil.xlsb')
        for _, row in df.iterrows():
            try:
                obj, created = Catalog.objects.get_or_create(
                    brand=row['brand'],
                    name=row['name'],
                    part_number=row['part_number'],
                    volume=row['volume'],
                    price_per_box=row['price_per_box'],
                    price_per_litre=row['price_per_litre'],
                    avalible_count=row['avalible_count'],
                    transit_count=row['transit_count'],
                    arrival_date=row['arrival_date'],
                    specification=row['specification']
                )
                if created:
                    success_count += 1
                if not created:
                    print(f'Catalog {obj} already exists in database')
            except IntegrityError as err:
                print(f'Error in row {row}: {err}')

        print(f'{success_count} entries were imported from .exel file.')
