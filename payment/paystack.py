from django.conf import settings
import requests
from requests.exceptions import ReadTimeout, ConnectionError
import json

class Paystack:
    PAYSTACK_SK = settings.PAYSTACK_SECRET_KEY
    base_url = "https://api.paystack.co/"
    
    def initialize_payment(self, email, amount):
        path = f'transaction/initialize'
        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SK}",
            'Content-Type': 'application/json',
        }
        url = self.base_url + path
        data = {
            "email": email,
            "amount": int(amount) * 100, # Paystack requirement
        }
        try:
            response = requests.post(url, data=json.dumps(data), headers=headers)
        except (ReadTimeout, ConnectionError):
            return 500, # this is to simulate error 500
        
        if response.status_code == 200:
            response_data = response.json()
            return response.status_code, response_data['data']['access_code'], response_data['data']['reference']
        else:
            print(response.status_code)
            print(response.json())
            return response.status_code,

    def verify_payment(self, ref, *args, **kwargs):
        path = f'transaction/verify/{ref}'
        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SK}",
            "Content-Type": "application/json",
        }
        url = self.base_url + path
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response_data['data']

        response_data = response.json()

        return response_data['status'], response_data['message']