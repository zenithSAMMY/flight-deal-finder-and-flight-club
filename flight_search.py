import dotenv
import os
import requests
import datetime as dt
from flight_data import FlightData
from pprint import pprint


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self) -> None:
        dotenv.load_dotenv()

        self.flight_api_key = os.getenv("flight_api_key")
        self.end_point = "https://tequila-api.kiwi.com"
        self.starting_point = "LON"

    def search_iataCode(self, cityname):
        params = {
            "term": cityname,
        }

        headers = {
            "apikey": self.flight_api_key,
        }

        response = requests.get(
            url=f"{self.end_point}/locations/query", params=params, headers=headers)
        response.raise_for_status()
        return response.json()["locations"][0]["code"]

    def search_for_flights(self, destination):
        today = dt.datetime.now()
        today = today.strftime("%d/%m/%Y")
        date_to_day = dt.datetime.now() + dt.timedelta(180)
        date_to_day = date_to_day.strftime("%d/%m/%Y")
        params = {
            "fly_from": self.starting_point,
            "fly_to": destination,
            "date_from": today,
            "date_to": date_to_day,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }

        headers = {
            "apikey": self.flight_api_key,
        }

        response = requests.get(
            url=f"{self.end_point}/v2/search", headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        try:
            flight_data = data["data"][0]
        except IndexError:
            try:
                params = {
                    "fly_from": self.starting_point,
                    "fly_to": destination,
                    "date_from": today,
                    "date_to": date_to_day,
                    "nights_in_dst_from": 7,
                    "nights_in_dst_to": 28,
                    "flight_type": "round",
                    "one_for_city": 1,
                    "max_stopovers": 1,
                    "curr": "GBP"
                }
                response = requests.get(
                    url=f"{self.end_point}/v2/search", headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
                flight_data = data["data"][0]
                flight_data_save = FlightData(
                    origin_city=flight_data["cityFrom"],
                    origin_airport=flight_data["flyFrom"],
                    destination_city=flight_data["cityTo"],
                    destination_airport=flight_data["flyTo"],
                    price=flight_data["conversion"]["GBP"],
                    out_date=flight_data["route"][0]["local_departure"].split("T")[
                        0],
                    return_date=flight_data["route"][2]["local_departure"].split("T")[
                        0],
                    step_over=1,
                    via_city=flight_data["route"][1]['cityFrom']
                )
                return flight_data_save

            except IndexError:
                print(f"No match flight to {destination}")
                return None
        else:
            flight_data_save = FlightData(
                origin_city=flight_data["cityFrom"],
                origin_airport=flight_data["flyFrom"],
                destination_city=flight_data["cityTo"],
                destination_airport=flight_data["flyTo"],
                price=flight_data["conversion"]["GBP"],
                out_date=flight_data["route"][0]["local_departure"].split("T")[
                    0],
                return_date=flight_data["route"][1]["local_departure"].split("T")[
                    0],
                step_over=0,
                via_city="",

            )

            return flight_data_save
