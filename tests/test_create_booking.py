import allure
import pytest
from pydantic import ValidationError
from requests.exceptions import HTTPError
from core.clients.endpoints import Endpoints
from core.models.booking import BookingResponse


@allure.feature('Test creating booking')
@allure.story('positive: creating booking with custom date')
def test_create_booking_with_custom_data(api_client):
    booking_data = {
        'firstname': 'Vasya',
        'lastname': 'Vasilyvich',
        'totalprice': 300,
        'depositpaid': True,
        'bookingdates': {
            'checkin': '2025-04-01',
            'checkout': '2025-04-15'
        },
        'additionalneeds': 'Dinner'
    }

    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f'Response validation failed: {e}')

    assert response['booking']['firstname'] == booking_data['firstname']
    assert response['booking']['lastname'] == booking_data['lastname']
    assert response['booking']['totalprice'] == booking_data['totalprice']
    assert response['booking']['depositpaid'] == booking_data['depositpaid']
    assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
    assert response['booking']['additionalneeds'] == booking_data['additionalneeds']


@allure.feature('Test creating booking')
@allure.story('positive: creating booking with random date')
def test_create_booking_with_random_date(api_client, generate_random_booking_data):
    with allure.step('Create booking'):
        response = api_client.create_booking(generate_random_booking_data)
        assert response['booking']['firstname'] == generate_random_booking_data['firstname']
        assert response['booking']['lastname'] == generate_random_booking_data['lastname']
        assert response['booking']['totalprice'] == generate_random_booking_data['totalprice']
        assert response['booking']['depositpaid'] == generate_random_booking_data['depositpaid']
        assert response['booking']['bookingdates']['checkin'] == generate_random_booking_data['bookingdates']['checkin']
        assert response['booking']['bookingdates']['checkout'] == generate_random_booking_data['bookingdates']['checkout']
        assert response['booking']['additionalneeds'] == generate_random_booking_data['additionalneeds']


@allure.feature('Test creating booking')
@allure.story('negative: missing required fields')
@pytest.mark.parametrize("invalid_data, missing_field", [
    ({  # отсутствует firstname
         'lastname': 'Doe',
         'totalprice': 200,
         'depositpaid': True,
         'bookingdates': {'checkin': '2025-05-01', 'checkout': '2025-05-10'},
         'additionalneeds': 'Lunch'
     }, 'firstname'),
    ({  # отсутствует bookingdates
         'firstname': 'John',
         'lastname': 'Doe',
         'totalprice': 200,
         'depositpaid': True,
         'additionalneeds': 'Lunch'
     }, 'bookingdates'),
    ({}, 'all fields')  # полностью пустой запрос
])
def test_create_booking_negative(api_client, invalid_data, missing_field):
    with allure.step(f'Attempt to create booking with missing/invalid field: {missing_field}'):
        with pytest.raises(HTTPError):
            api_client.create_booking(invalid_data)
