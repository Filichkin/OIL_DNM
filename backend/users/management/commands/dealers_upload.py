from django.core.management.base import BaseCommand
from django.db import IntegrityError
import pandas as pd

from oil_dnm import settings
from users.models import Dealer


class Command(BaseCommand):
    help = 'Import data from exel file into Dealer model in database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Path to file')

    def handle(self, *args, **options):
        success_count = 0
        print('Loading data...')
        df = pd.read_excel(f'{settings.BASE_DIR}/data/dealers_base.xlsx')
        df.columns = [
            'sap_code',
            'name',
            'rs_code',
            'inn',
            'city',
            'legal_address',
            'address'
            ]
        for _, row in df.iterrows():
            try:
                obj, created = Dealer.objects.get_or_create(
                    name=row['name'],
                    rs_code=row['rs_code'],
                    inn=row['inn'],
                    city=row['city'],
                    legal_address=row['legal_address'],
                    address=row['address']
                )
                if created:
                    success_count += 1
                if not created:
                    print(f'Dealer {obj} already exists in database')
            except IntegrityError as err:
                print(f'Error in row {row}: {err}')

        print(f'{success_count} entries were imported from .exel file.')
