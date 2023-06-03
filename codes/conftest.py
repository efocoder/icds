from rest_framework.test import APIClient
import pytest

from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate():
        return api_client.force_authenticate(user=User(is_staff=False))

    return do_authenticate
