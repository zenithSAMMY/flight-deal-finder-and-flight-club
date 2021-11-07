import requests
import os


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self) -> None:
        self.end_point = os.environ['sheety_end_point']

    def get_data(self):
        response = requests.get(url=f"{self.end_point}/prices")
        response.raise_for_status()
        data = response.json()
        return data["prices"]

    def get_user_email(self):
        response = requests.get(url=f"{self.end_point}/users")
        response.raise_for_status()
        data = response.json()
        return data["users"]

    def update_data_iataCode(self, data):
        params = {
            "price": {
                "iataCode": data["iataCode"],
            }
        }
        response = requests.put(
            url=f"{self.end_point}/prices/{data['id']}", json=params)
        response.raise_for_status()

    def update_data_price(self, data):
        params = {
            "price": {
                "lowestPrice": data["lowestPrice"],
            }
        }
        response = requests.put(
            url=f"{self.end_point}/prices/{data['id']}", json=params)
        response.raise_for_status()
