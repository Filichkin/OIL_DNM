from django.core.management.base import BaseCommand
from django.db import IntegrityError

from oil_dnm import settings
from catalog.models import Catalog