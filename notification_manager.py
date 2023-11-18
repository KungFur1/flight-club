import smtplib
from email.message import EmailMessage
import imghdr
from flight_data import FlightData
from email_unsubscribe_secret import EmailUnsubscribeSecret
from flask import url_for, current_app
import config


# with open('email/images/airplane-dots.png', 'rb') as f:
#     airplane_file_data = f.read()
#     airplane_file_type = imghdr.what(f.name)
#     airplane_file_name = f.name


with open("email/flight_mail_start.html") as f:
    flight_email_start = f.read()

with open("email/flight_mail_middle.html") as f:
    flight_email_middle = f.read()

with open("email/flight_mail_end.html") as f:
    flight_email_end = f.read()



def format_email_subject(trip_data_list: list[FlightData]) -> str:
    trip_0: FlightData
    trip_0 = trip_data_list[0]
    if len(trip_data_list) == 1:
        return f"Flight found! {trip_0.city_from} --> {trip_0.city_to}"
    elif len(trip_data_list) > 1:
        return f"Multiple flights found! {trip_0.city_from} --> {trip_0.city_to}"


def format_email_body(trip_data_list: list[FlightData], secret: EmailUnsubscribeSecret) -> str:

    def format_route_info(trip: FlightData) -> str:
        trip_text = f"{trip.country_form}, {trip.city_from}  -->  {trip.country_to}, {trip.city_to} \n" \
                    f"Price: {trip.price_eur}eur  Seats left: {trip.seats_left} \n" \
                    f"Departure: {trip.fly_from_iata} {trip.local_departure} \n" \
                    f"Arrival: {trip.fly_to_iata} {trip.local_arrival} \n"
        if trip.is_round_trip:
            trip_text += f"Come back to {trip.city_from} at: {trip.comeback_local_arrival} \n"
        trip_text += f"Number of flights: {trip.route_len} \n"
        return trip_text

    trip_0: FlightData
    trip_0 = trip_data_list[0]
    if len(trip_data_list) == 1:
        message = f"Found a route from {trip_0.city_from} to " \
                  f"{trip_0.city_to}{' and back' if trip_0.is_round_trip else ''}! \n"
    elif len(trip_data_list) > 1:
        message = f"Found {len(trip_data_list)} routes from {trip_0.city_from} to " \
                  f"{trip_0.city_to}{' and back' if trip_0.is_round_trip else ''}! \n"

    message += "\n"
    message += format_route_info(trip_data_list[0])
    message += "\n"
    if len(trip_data_list) > 1:
        message += "\n"
        message += format_route_info(trip_data_list[1])
        message += "\n"
    if len(trip_data_list) > 2:
        message += "\n"
        message += format_route_info(trip_data_list[2])
        message += "\n"
        if len(trip_data_list) > 3:
            message += f"... {len(trip_data_list) - 3} more routes ..."

    message += "\n" + config.BASE_URL + "/unsubscribe" + f"/{secret.email}" + f"/{secret.unsubscribe_secret}"

    return message


# IMPLEMENT MULTIPLE FLIGHT INFO!!!
def render_flight_found_template(flights:list[FlightData], secret: EmailUnsubscribeSecret) -> str:
    # Variables that need to be replaced are in double brackets [[VAR_NAME]]
    # Variable names: TITLE, FROM_CITY, FROM_IATA, TO_CITY, TO_IATA, PRICE, SEATS_LEFT, DEPARTURE_DATE, ARRIVAL_DATE,
    # RETURN_DATE, NUMBER_OF_FLIGHTS, UNSUBSCRIBE, ROUTE_NUMBER
    start = flight_email_start
    middle = ""
    end = flight_email_end
    start = start.replace("[[TITLE]]", f"Found {len(flights)} routes to..")
    start = start.replace("[[FROM_CITY]]", flights[0].city_from)
    start = start.replace("[[FROM_IATA]]", flights[0].fly_from_iata)
    start = start.replace("[[TO_CITY]]", flights[0].city_to)
    start = start.replace("[[TO_IATA]]", flights[0].fly_to_iata)
    end = end.replace("[[UNSUBSCRIBE]]", config.BASE_URL + "/unsubscribe" + f"/{secret.email}" + f"/{secret.unsubscribe_secret}")

    i = 1
    for flight in flights:
        one_flight_info = flight_email_middle
        one_flight_info = one_flight_info.replace("[[ROUTE_NUMBER]]", f"{i}")
        one_flight_info = one_flight_info.replace("[[FROM_CITY]]", flight.city_from)
        one_flight_info = one_flight_info.replace("[[FROM_IATA]]", flight.fly_from_iata)
        one_flight_info = one_flight_info.replace("[[TO_CITY]]", flight.city_to)
        one_flight_info = one_flight_info.replace("[[TO_IATA]]", flight.fly_to_iata)
        one_flight_info = one_flight_info.replace("[[PRICE]]", f"{flight.price_eur}")
        one_flight_info = one_flight_info.replace("[[SEATS_LEFT]]", f"{flight.seats_left}")
        one_flight_info = one_flight_info.replace("[[DEPARTURE_DATE]]", flight.local_departure)
        one_flight_info = one_flight_info.replace("[[ARRIVAL_DATE]]", flight.local_arrival)
        one_flight_info = one_flight_info.replace("[[RETURN_DATE]]", flight.comeback_local_arrival if flight.is_round_trip else "One way flight")
        one_flight_info = one_flight_info.replace("[[NUMBER_OF_FLIGHTS]]", f"{flight.route_len}")
        middle += one_flight_info
        i += 1

    return start + middle + end


def sendFoundFlights(flights:list[FlightData], secret: EmailUnsubscribeSecret):
    sender_addrs = "learnpythonone@gmail.com"
    app_password = "hyoqizaryjzerluw"

    msg = EmailMessage()
    msg['Subject'] = format_email_subject(flights)
    msg['From'] = sender_addrs
    msg['To'] = secret.email
    msg.set_content(format_email_body(flights, secret))
    msg.add_alternative(render_flight_found_template(flights,secret), subtype="html")
    # msg.add_attachment(airplane_file_data, maintype="image", subtype=airplane_file_type, filename=airplane_file_name)

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=sender_addrs, password=app_password)
        connection.send_message(msg=msg)
