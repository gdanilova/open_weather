import requests
import pytest

BASE_URL = 'https://restful-booker.herokuapp.com/booking'
AUTH_URL = 'https://restful-booker.herokuapp.com/auth'
STATUS_OK = 200

@pytest.fixture(scope='module')
def auth_token():
    payload = {
            "username": "admin",
            "password": "password123"
    }
    response = requests.post(AUTH_URL, json=payload)
    response_data = response.json()
    token = response_data['token']
    assert response.status_code == STATUS_OK
    yield token

@pytest.fixture(scope='module')
def booking_id():
    payload = {
        "firstname": "John",
        "lastname": "Smith",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Breakfast"
    }
    response = requests.post(BASE_URL, json=payload)
    booking_id = response.json()['bookingid']
    assert response.status_code == 200
    yield booking_id



def test_get_all_bookings():
    response = requests.get(BASE_URL)
    print(f'\n{len(response.json())}')
    assert response.status_code == 200
    key = 'Connection'
    assert key in response.headers

def test_get_booking_with_id():
    response = requests.get(f'{BASE_URL}/1')
    response_data = response.json()
    expected_keys = ['firstname', 'lastname', 'totalprice', 'depositpaid', 'bookingdates']
    for key in expected_keys:
        assert key in response_data.keys()
    print(f'\n{response_data}')


def test_create_booking(booking_id):
    response = requests.get(f'{BASE_URL}/{booking_id}')
    assert response.status_code == 200
    assert response.json()['firstname'] == 'John'


def test_user_autorization():
    payload = {
            "username": "admin",
            "password": "password123"
    }
    response = requests.post(AUTH_URL, json=payload)
    response_data = response.json()
    assert response.status_code == STATUS_OK
    assert 'token' in response_data

def test_update_booking(booking_id, auth_token):
    payload = {
        "firstname": "John",
        "lastname": "Smith",
        "totalprice": 500,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Lunch"
    }
    headers = {'Cookie': f'token={auth_token}'}

    response = requests.put(f'{BASE_URL}/{booking_id}', json=payload, headers=headers)
    assert response.status_code == 200

    response_get = requests.get(f'{BASE_URL}/{booking_id}')
    response_data = response_get.json()
    assert response.status_code == 200
    assert response_data['totalprice'] == payload['totalprice']
    assert response_data['additionalneeds'] == payload['additionalneeds']

def test_delete_booking(booking_id, auth_token):
    headers = {'Cookie': f'token={auth_token}'}
    response = requests.delete(f'{BASE_URL}/{booking_id}', headers=headers)
    assert response.status_code == 201
    response_get = requests.get(f'{BASE_URL}/{booking_id}')
    assert response_get.status_code == 404