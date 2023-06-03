import pytest
from model_bakery import baker
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnList

from codes.models import Code, Category


@pytest.fixture
def create_single_code(api_client):
    def do_create_single_code(code):
        return api_client.post('/codes/', code)

    return do_create_single_code


@pytest.fixture
def retrieve_code(api_client):
    def do_retrieve_code(code_id=None):
        if code_id is not None:
            return api_client.get(f'/codes/{code_id}/')
        else:
            return api_client.get('/codes/')

    return do_retrieve_code


@pytest.mark.django_db
class TestCreateCode:
    def test_if_user_is_not_authorized_return_401(self, create_single_code):
        response = create_single_code({})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_invalid_return_400(self, create_single_code, authenticate):
        authenticate()
        response = create_single_code({})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_return_201(self, create_single_code, authenticate):
        authenticate()

        response = create_single_code(
            {'diagnosis_code': 0, 'full_code': 'A000', 'abbrev_desc': 'simple abbrev description',
             'full_desc': 'full description for record', 'category': baker.make(Category).id, 'status': 'active'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveCode:
    def test_if_user_is_not_authorized_return_401(self, retrieve_code):
        response = retrieve_code()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authorized_return_200_for_list(self, retrieve_code, authenticate):
        authenticate()
        baker.make(Code, _quantity=50)

        response = retrieve_code()

        assert type(response.data['results']) == ReturnList
        assert len(response.data['results']) == 20
        assert {'results'}.issubset(response.data)
        assert {'next'}.issubset(response.data)

    def test_get_code_by_valid_id(self, authenticate, retrieve_code, create_single_code):
        authenticate()

        code = create_single_code({'diagnosis_code': 0, 'full_code': 'A000', 'abbrev_desc': 'simple abbrev description',
                                   'full_desc': 'full description for record', 'category': baker.make(Category).id,
                                   'status': 'active'})

        response = retrieve_code(code.data['id'])

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, dict)

    def test_update_code(self, authenticate, api_client, create_single_code):
        authenticate()

        code = create_single_code({'diagnosis_code': 0, 'full_code': 'A000', 'abbrev_desc': 'simple abbrev description',
                                   'full_desc': 'full description for record', 'category': baker.make(Category).id,
                                   'status': 'active'})

        response = api_client.patch(f"/codes/{code.data['id']}/", {'diagnosis_code': '2', 'full_code': 'A002'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['diagnosis_code'] == '2'
        assert response.data['full_code'] == 'A002'

    def test_delete_code(self, authenticate, api_client, create_single_code):
        authenticate()

        code = create_single_code({'diagnosis_code': 0, 'full_code': 'A000', 'abbrev_desc': 'simple abbrev description',
                                   'full_desc': 'full description for record', 'category': baker.make(Category).id,
                                   'status': 'active'})

        response = api_client.delete(f"/codes/{code.data['id']}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
