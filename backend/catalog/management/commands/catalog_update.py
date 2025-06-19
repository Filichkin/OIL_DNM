from django.core.management.base import BaseCommand
from django.db import IntegrityError

from oil_dnm import settings
from catalog.models import Catalog
from .utils import excel_preprocess


class Command(BaseCommand):
    help = 'Update data from exel file into Catalog model in database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Path to file')

    def handle(self, *args, **options):
        updated_count = 0
        created_count = 0
        print('Loading data...')
        df = excel_preprocess(f'{settings.BASE_DIR}/data/PriceOil.xlsb')
        for _, row in df.iterrows():
            try:
                updated, created = Catalog.objects.update_or_create(
                    part_number=row['part_number'],
                    defaults={
                        'price_per_litre': row['price_per_litre'],
                        'price_per_box': row['price_per_box'],
                        'avalible_count': row['avalible_count'],
                        'transit_count': row['transit_count'],
                        'arrival_date': row['arrival_date'],
                        },
                    create_defaults={
                        'brand': row['brand'],
                        'name': row['name'],
                        'part_number': row['part_number'],
                        'volume': row['volume'],
                        'price_per_box': row['price_per_box'],
                        'price_per_litre': row['price_per_litre'],
                        'avalible_count': row['avalible_count'],
                        'transit_count': row['transit_count'],
                        'arrival_date': row['arrival_date'],
                        'specification': row['specification']
                        }
                )
                if updated:
                    updated_count += 1
                if created:
                    created_count += 1
                    print(f'Catalog {created} was added to database')
            except IntegrityError as err:
                print(f'Error in row {row}: {err}')

        print(f'{updated_count} entries were updated from .exel file.')
        print(f'{created_count} entries were created from .exel file.')
