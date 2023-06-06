import csv
import logging
import os

from pathlib import Path
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "diagnosis.settings")
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR.as_posix())
django.setup()

from codes.models import Category
from djoser.serializers import UserCreateSerializer

logger = logging.getLogger('django')


def load_categories():
    try:
        file = open(f'{BASE_DIR}/utils/categories.csv', errors='ignore')
        reader = csv.reader(file)
        objs = []

        for row in reader:
            (code, title) = row
            objs.append(Category(category_code=code, title=title, status='active'))
        Category.objects.bulk_create(objs)
    except Exception as e:
        logger.error(e)


def create_test_user():
    logger.info('creating test user...')
    user = UserCreateSerializer(data={'email': 'testemail@mail.com', 'username': 'testuser', 'password': 'pas12345'})
    if user.is_valid(raise_exception=True):
        user.save()


def main():
    load_categories()
    create_test_user()


main()
