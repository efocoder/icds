import csv
import logging
import os

from celery import shared_task

from pathlib import Path
import sys
import django

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR.as_posix())
django.setup()

from codes.models import Code, Category

logger = logging.getLogger('django')


@shared_task()
def create_bulk_codes(data):
    logger.info('inserting bulk...')
    code_list = []
    try:
        file = open(f"{BASE_DIR}/tmp/{data['filename']}", errors='ignore')
        reader = csv.reader(file)

        for row in reader:
            (cat_code, diagnosis_code, full_code, abbrev_desc, full_desc) = row[:5]

            code_list.append(
                Code(category=Category.objects.get(category_code=cat_code),
                     diagnosis_code=diagnosis_code,
                     full_code=full_code, abbrev_desc=abbrev_desc, full_desc=full_desc, status='active'))

        Code.objects.bulk_create(code_list)
    except Exception as e:
        logger.error(e)
