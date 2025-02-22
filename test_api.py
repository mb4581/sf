import pytest
import json

from api import PetFriends

pf = PetFriends()
valid_email = 'nigger@nigger.ni'
valid_password = 'nigger'


@pytest.fixture(scope='class')
def auth_key(email=valid_email, password=valid_password) -> json:
    status, result = pf.get_api_key(email=email, password=password)
    assert status == 200
    assert 'key' in result
    return result['key']


@pytest.mark.parametrize("password", ['123456'], ids=['invalid pass'])
@pytest.mark.parametrize("email", ['ffff@hhhh.gg'], ids=['invalid email'])
def test_auth_should_fail(email, password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_list_pets(auth_key):
    status, result = pf.get_list_of_pets(auth_key)
    assert status == 200 and len(result['pets']) > 0


def test_list_my_pets(auth_key):
    status, result = pf.get_list_of_pets(auth_key, 'my_pets')
    assert status == 200 and len(result['pets']) > 0


def test_cant_add_negative_age(auth_key):
    status, result = pf.add_new_pet_without_photo(auth_key, 'Кот', 'Кот', -99)
    assert status == 400


def test_cant_add_huge_age(auth_key):
    status, result = pf.add_new_pet_without_photo(auth_key, 'Кот', 'Кот', 9999)
    assert status == 400


def test_cant_add_extra_huge_age(auth_key):
    status, result = pf.add_new_pet_without_photo(auth_key, 'Кот', 'Кот', 9999999999999999999999999)
    assert status == 400


def test_cant_add_empty_name(auth_key):
    status, result = pf.add_new_pet_without_photo(auth_key, '', '-', 10)
    assert status == 400


def test_cant_add_empty_type(auth_key):
    status, result = pf.add_new_pet_without_photo(auth_key, '-', '', 10)
    assert status == 400


def test_cant_add_long_type(auth_key):
    name = 'ы' * 990
    status, result = pf.add_new_pet_without_photo(auth_key, '-', name, 10)
    assert status == 400
