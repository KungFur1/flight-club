import requests
import datetime
import config
from flight_data import FlightData


# Cannot exceed 2000 for legal reasons!!!
tequila_api_calls_amount = 0
def securityCheck():
    global tequila_api_calls_amount
    tequila_api_calls_amount += 1
    if tequila_api_calls_amount >= 2000:
        print("CRITICAL ERROR!")
        print("Tequila API calls amount is greater than 2000!")
        print("END PROGRAM NOW!")
        quit(2000)


def get_iata_code(city: str) -> str | None:
    """Will throw CommunicationWithServerError if communication with server is unsuccessful,
    returns None, if 0 locations were found"""

    securityCheck()

    args = {
        "term": city,
        "locale": "en-US",
        "location_types": "airport"
    }
    response = requests.get(url=config.TEQUILA_LOCATIONS_ENDPOINT, params=args, headers=config.TEQUILA_AUTHORIZATION_HEADER)
    try:
        response.raise_for_status()
        locations_list = response.json()["locations"]
        if len(locations_list) > 0:
            return locations_list[0]["code"]
        else:
            return None
    except requests.exceptions.HTTPError as e:
        raise ConnectionError(f"HTTP error: {e.response}")
    except KeyError:
        raise ConnectionError("Bad response format from Tequila server.")


def find_one_way_flight(fly_from: str, fly_to: str, date_from: datetime.date,
                        date_to: datetime.date, price_to: int) -> list[FlightData]:
    args = {
        "fly_from": fly_from,
        "fly_to": fly_to,
        "date_from": date_from.strftime("%d/%m/%Y") if date_from >= datetime.date.today() else datetime.date.today(),
        "date_to": date_to.strftime("%d/%m/%Y"),
        "price_to": price_to,
    }
    return get_flight(args)


def find_round_trip_flight(fly_from: str, fly_to: str, date_from: datetime.date, date_to: datetime.date, price_to: int,
                           nights_in_dst_from: int, nights_in_dst_to: int) -> list[FlightData]:
    args = {
        "fly_from": fly_from,
        "fly_to": fly_to,
        "date_from": date_from.strftime("%d/%m/%Y") if date_from >= datetime.date.today() else datetime.date.today(),
        "date_to": date_to.strftime("%d/%m/%Y"),
        "price_to": price_to,
        "nights_in_dst_from": nights_in_dst_from,
        "nights_in_dst_to": nights_in_dst_to
    }
    return get_flight(args)


def get_flight(args) -> list[FlightData]:
    securityCheck()

    response = requests.get(url=config.TEQUILA_SEARCH_ENDPOINT, params=args, headers=config.TEQUILA_AUTHORIZATION_HEADER)
    try:
        response.raise_for_status()
        flight_data_list = response.json()["data"]
    except requests.exceptions.HTTPError as e:
        raise ConnectionError(f"HTTP error: {e.response}")
    except KeyError:
        raise ConnectionError(f"Bad response from the Tequila server")
    else:
        flight_list = []
        for flight_data in flight_data_list:
            flight_list.append(FlightData(flight_data))
        return flight_list
