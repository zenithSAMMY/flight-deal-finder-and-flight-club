# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from pprint import pprint
import os
from twilio.rest import Client
from notification_manager import NotificationManager

data_manager = DataManager()
flight_search = FlightSearch()
sheet_data = data_manager.get_data()
notification_manager = NotificationManager()

user_email_data = data_manager.get_user_email()

for data in sheet_data:
    flight_data = flight_search.search_for_flights(data["iataCode"])
    if flight_data:
        if flight_data.price < data["lowestPrice"]:
            for user in user_email_data:
                notification_manager.send_emails(flight_data, user["email"])


# if flight_data.price < data["lowestPrice"]:
#     # update lowest price
#     data["lowestPrice"] = flight_data.price
#     data_manager.update_data_price(data)


# UPDATE iadaCode
# for data in sheet_data:
#     iataCode = flight_search.search_iataCode(data["city"])
#     data["iataCode"] = iataCode

# for data in sheet_data:
#     data_manager.update_data_iataCode(data)
