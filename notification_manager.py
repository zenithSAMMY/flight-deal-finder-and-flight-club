import os
from twilio.rest import Client
import smtplib


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self) -> None:
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.client = Client(account_sid, auth_token)

    def send_message(self, flight_data):
        if flight_data.stop_overs > 0:
            message = self.client.messages \
                .create(
                    body=f"Low price alert! Only £{flight_data.price} to fly from {flight_data.origin_city}-{flight_data.origin_airport} to {flight_data.destination_city}-{flight_data.destination_airport}, from {flight_data.out_date} to {flight_data.return_date}.\n\nFlight has {flight_data.stop_overs} stop over, via {flight_data.via_city}",
                    from_=os.environ['TWILIO_phonenumber'],
                    to=os.environ['my_phonenumber']
                )
        else:
            message = self.client.messages \
                .create(
                    body=f"Low price alert! Only £{flight_data.price} to fly from {flight_data.origin_city}-{flight_data.origin_airport} to {flight_data.destination_city}-{flight_data.destination_airport}, from {flight_data.out_date} to {flight_data.return_date}.",
                    from_=os.environ['TWILIO_phonenumber'],
                    to=os.environ['my_phonenumber']
                )
        print(message.sid)
        print(message.status)

    def send_emails(self, flight_data, email):
        my_email = os.environ["my_email"]
        password = os.environ["password"]

        if flight_data.stop_overs > 0:
            content = f"Low price alert! Only £{flight_data.price} to fly from {flight_data.origin_city}-{flight_data.origin_airport} to {flight_data.destination_city}-{flight_data.destination_airport}, from {flight_data.out_date} to {flight_data.return_date}.\n\nFlight has {flight_data.stop_overs} stop over, via {flight_data.via_city}\n"
        else:
            content = f"Low price alert! Only £{flight_data.price} to fly from {flight_data.origin_city}-{flight_data.origin_airport} to {flight_data.destination_city}-{flight_data.destination_airport}, from {flight_data.out_date} to {flight_data.return_date}.\n"

        content = content.encode('utf-8')
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email,
                                to_addrs=email, msg="Subject:New Low Price Flight!" + content)
