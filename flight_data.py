class FlightData:

    def __init__(self, flight_data: dict):
        """Any unknown parameters are set to None"""

        self.id = flight_data.get("id")
        self.price_eur = flight_data.get("price")
        self.seats_left = flight_data["availability"].get("seats") if \
            flight_data.get("availability") is not None else None
        self.fly_from_iata = flight_data.get("flyFrom")
        self.fly_to_iata = flight_data.get("flyTo")
        self.city_from = flight_data.get("cityFrom")
        self.city_to = flight_data.get("cityTo")
        self.country_form = flight_data["countryFrom"].get("name") if \
            flight_data.get("countryFrom") is not None else None
        self.country_to = flight_data["countryTo"].get("name") if flight_data.get("countryTo") is not None else None
        self.airlines = flight_data.get("airlines")
        self.raw_route_data = flight_data.get("route")

        self.local_arrival = flight_data.get("local_arrival")
        self.local_departure = flight_data.get("local_departure")
        self.utc_arrival = flight_data.get("utc_arrival")
        self.utc_departure = flight_data.get("utc_departure")
        self.route_len = len(flight_data.get("route")) if flight_data.get("route") is not None else None

        # Check if flight is a round trip and if it is then extract come back route data
        self.is_round_trip = False
        if self.route_len is not None and self.route_len > 1:
            for flight in self.raw_route_data:
                flight_destination_iata = flight.get("flyTo")
                if flight_destination_iata == self.fly_from_iata:
                    self.is_round_trip = True

        if self.is_round_trip == True:
            for flight in self.raw_route_data:
                flight_origin_iata = flight.get("flyFrom")
                flight_destination_iata = flight.get("flyTo")
                if flight_origin_iata == self.fly_to_iata:
                    self.comeback_local_departure = flight.get("local_departure")
                    self.comeback_utc_departure = flight.get("utc_departure")
                if flight_destination_iata == self.fly_from_iata:
                    self.comeback_local_arrival = flight.get("local_arrival")
                    self.comeback_utc_arrival = flight.get("utc_arrival")



    def print(self):
        if self.is_round_trip:
            print(f"Round trip route found! ID:  {self.id} \n"
                  f"Fly from {self.country_form}, {self.city_from}({self.fly_from_iata}) "
                  f"to {self.country_to}, {self.city_to}({self.fly_to_iata}) with {self.airlines} airlines \n"
                  f"Price is:  {str(self.price_eur).zfill(4)}  Seats left:  {str(self.seats_left).zfill(3)}  "
                  f"Total flights:  {self.route_len} \n"
                  f"Local arrival and departure times:  {self.local_departure}    {self.local_arrival} \n"
                  f"UTC arrival and departure times:  {self.utc_departure}    {self.utc_arrival} \n"
                  f"Come back flight local arrival and departure times:  {self.comeback_local_departure}    {self.comeback_local_arrival} \n"
                  f"Come back flight UTC arrival and departure times:  {self.comeback_utc_departure}    {self.comeback_utc_arrival} \n")
        else:
            print(f"One way route found! ID:  {self.id} \n"
                  f"Fly from {self.country_form}, {self.city_from}({self.fly_from_iata}) "
                  f"to {self.country_to}, {self.city_to}({self.fly_to_iata}) with {self.airlines} airlines \n"
                  f"Price is:  {str(self.price_eur).zfill(4)}  Seats left:  {str(self.seats_left).zfill(3)}  "
                  f"Total flights:  {self.route_len} \n"
                  f"Local arrival and departure times:  {self.local_departure}    {self.local_arrival} \n"
                  f"UTC arrival and departure times:  {self.utc_departure}    {self.utc_arrival} \n")
