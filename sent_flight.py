import datetime


class SentFlight:
    def __init__(self, id:int, created_at:datetime.date, flight_entry_id:int, price:float, departure_date:datetime.date):
        self.id = id
        self.created_at = created_at
        self.flight_entry_id = flight_entry_id
        self.price = price
        self.departure_date = departure_date


    def print(self):
        print(f"id {self.id} created_at {self.created_at} flight_entry_id {self.flight_entry_id} price {self.price} "
              f"departure_date {self.departure_date} \n")

