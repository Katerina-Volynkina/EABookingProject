import allure

@allure.feature('Test Create')
@allure.story('Test Create_booking')
def test_create_booking(api_client, generate_random_booking_data):
    with allure.step('Create booking'):
        response = api_client.create_booking(generate_random_booking_data)
        assert response['booking']['firstname'] == generate_random_booking_data['firstname']
        assert response['booking']['lastname'] == generate_random_booking_data['lastname']
        assert response['booking']['totalprice'] == generate_random_booking_data['totalprice']
        assert response['booking']['depositpaid'] == generate_random_booking_data['depositpaid']
        assert response['booking']['bookingdates']['checkin'] == generate_random_booking_data['bookingdates']['checkin']
        assert response['booking']['bookingdates']['checkout'] == generate_random_booking_data['bookingdates']['checkout']
        assert response['booking']['additionalneeds'] == generate_random_booking_data['additionalneeds']