import datetime
import flight_search


class FlightEntry:

    def __init__(self, email: str, departure_iata: str, arrival_iata: str, earliest_departure_date: datetime.date,
                 latest_departure_date: datetime.date, round_trip: bool, shortest_stay: int, longest_stay: int,
                 highest_price: int, id: int = None, created_at: datetime.date = None):
        self.departure_iata = departure_iata
        self.arrival_iata = arrival_iata
        self.earliest_departure_date = earliest_departure_date
        self.latest_departure_date = latest_departure_date
        self.round_trip = round_trip
        self.shortest_stay = shortest_stay
        self.longest_stay = longest_stay
        self.email = email
        self.highest_price = highest_price
        # These fields are given value by database. If entry just came from web, they should be left default
        self.id = id
        self.created_at = created_at


    def print(self):
        print(f"{self.departure_iata} --> {self.arrival_iata} \n"
              f"Departure period: {self.earliest_departure_date}  -  {self.latest_departure_date} \n"
              f"{f'Days to stay: From {self.shortest_stay} To {self.longest_stay}' if self.round_trip else 'One way trip'} \n"
              f"Email: {self.email} \n"
              f"Highest price: {self.highest_price}eur \n"
              f"Id: {self.id} Created at: {self.created_at} \n\n")



def checkFormMakeFlightEntry(form) -> FlightEntry:
    '''If data is incorrect an error will be raised'''
    departure_iata = flight_search.get_iata_code(form['departure_city'])
    arrival_iata = flight_search.get_iata_code(form['arrival_city'])
    earliest_departure_date = datetime.datetime.strptime(form['earliest_departure_date'], '%Y-%m-%d')
    latest_departure_date = datetime.datetime.strptime(form['latest_departure_date'], '%Y-%m-%d')
    round_trip = True if form.get('round_trip') is not None else False
    if round_trip:
        shortest_stay = int(form['shortest_stay'])
        longest_stay = int(form['longest_stay'])
    else:
        shortest_stay = None
        longest_stay = None
    email = form['email']
    highest_price = int(form['highest_price'])

    # Checking if data is correct
    if departure_iata is None and arrival_iata is None:
        raise NameError("Failed to find departure airport and arrival airport")
    elif departure_iata is None:
        raise NameError("Failed to find departure airport")
    elif arrival_iata is None:
        raise NameError("Failed to find arrival airport")

    if earliest_departure_date > latest_departure_date:
        raise Exception("Earliest departure date cannot be later than latest departure date")

    if round_trip and shortest_stay > longest_stay:
        raise Exception("Shortest stay time cannot be longer than longest stay time")

    if round_trip and (shortest_stay < 0 or longest_stay < 0):
        raise Exception("Shortest stay time cannot be longer than longest stay time")

    if highest_price <= 0:
        raise Exception("Price cannot be negative or zero")

    return FlightEntry(email, departure_iata, arrival_iata, earliest_departure_date, latest_departure_date,
         round_trip, shortest_stay, longest_stay, highest_price)