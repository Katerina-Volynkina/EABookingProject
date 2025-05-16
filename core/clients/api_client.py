import requests
import os
from requests.auth import HTTPBasicAuth
from core.settings.environments import Environment
from core.clients.endpoints import Endpoints
from core.settings.config import Users, Timeouts
import allure
from dotenv import load_dotenv

load_dotenv()


class APIClient:
    def __init__(self):
        environment_str = os.getenv('ENVIRONMENT')
        try:
            environment = Environment[environment_str]
        except KeyError:
            raise ValueError(f'Unsupported environment value: {environment_str}')

        self.base_url = self.get_base_url(environment)
        self.session = requests.Session()
        self.session.headers = {
            'Content-Type':'application/json',
            'accept': '*/*'
        }

    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv("TEST_BASE_URL")
        elif environment == Environment.PROD:
            return os.getenv("PROD_BASE_URL")
        else:
            raise ValueError(f"Unsupported environment: {environment}")


    def get(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.session.headers,params=params)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def post(self, endpoint, data=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.post(url, headers=self.session.headers,json=data)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def ping(self):
        with allure.step('Ping api client'):
            url =f'{self.base_url}{Endpoints.PING_ENDPOINT.value}'
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step('Assert status code'):
            assert  response.status_code == 201, f'Expected status 201, but got {response.status_code}'
        return response.status_code

    def auth(self):
        with allure.step('Getting autenticate'):
            url = f'{self.base_url}{Endpoints.AUTH_ENDPOINT.value}'
            payload = {'username': Users.USERNAME.value, 'password': Users.PASSWORD.value}
            response = self.session.post(url, json=payload, timeout=Timeouts.TIMEOUT.value)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f'Expected status 200, but got {response.status_code}'
        token = response.json().get('token')
        with allure.step('Updating header with authorization'):
            self.session.headers.update({'Authorization': f"Bearer{token}"})

    def get_booking_by_id(self, booking_id):
        with allure.step('Getting booking ID'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}'
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f'Expected status 200, but got {response.status_code}'
        return response.json()

    def delete_booking(self, booking_id):
        with allure.step('Delete booking'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}'
            response = self.session.delete(url, auth=HTTPBasicAuth(Users.USERNAME.value, Users.PASSWORD.value))
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 201, f'Expected status 201, but got {response.status_code}'
        return response.status_code == 201

    def create_booking(self, booking_data):
        with allure.step('Create booking'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}'
            response = self.session.post(url, json =booking_data)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f'Expected status 201, but got {response.status_code}'

        return response.json()

    def get_booking_ids(self, params=None):
        with allure.step('Getting object with bookings'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}'
            response = self.session.get(url, params=params)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'
        return response.json()

    def update_booking(self, booking_id, booking_data):
        with allure.step('Update booking'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}'
            response = self.session.put(url, auth=HTTPBasicAuth(Users.USERNAME.value, Users.PASSWORD.value), json=booking_data)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f'Expected status 200, but got {response.status_code}'
        return response.json()

    def partial_update_booking(self, booking_id, patch_data):
        with allure.step('Partial update booking') :
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}'
            response = self.session.patch(url, json=patch_data)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f'Expected status 200, but got {response.status_code}'
        return response.json()



