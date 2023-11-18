import database_manager
import flight_search
import datetime
import notification_manager
from flight_entry import FlightEntry
from sent_flight import SentFlight
import email_unsubscribe_secret
from flight_data import FlightData


# Also deletes old entries
# Should be called periodically like Every Hour
def checkEveryFlight():
    # Read all flight entries and try to find a flight for all of them
    all_flight_entries:[FlightEntry] = database_manager.getAllFlightEntries()
    for entry in all_flight_entries:

        # Checking available flights
        # If entry is old - delete instead of search for flight
        if entry.latest_departure_date > datetime.date.today():
            found_flights = findFlightsForEntry(entry)
        else:
            database_manager.deleteOldEntry(entry)
            # Move on to other entry
            continue

        if len(found_flights) == 0:
            continue

        # Here every newly found flight is compared to old sent flights in order not to send similar flights
        previously_sent_flights:[SentFlight] = database_manager.getAllSentFlightsWithEntryId(entry.id)
        flights_to_be_sent:[FlightData] = []
        amount_of_checked_flights = 0
        for flight in found_flights:
            if amount_of_checked_flights >= 4:
                break
            amount_of_checked_flights += 1

            flight_should_be_sent = True
            for previously_sent_flight in previously_sent_flights:
                departure_date = datetime.datetime.strptime(flight.local_departure.split('T')[0],
                                                            '%Y-%m-%d').date()
                time_between_flights = previously_sent_flight.departure_date - departure_date if (previously_sent_flight.departure_date > departure_date) else departure_date - previously_sent_flight.departure_date
                if time_between_flights.days < 7 and previously_sent_flight.price <= flight.price_eur:
                    flight_should_be_sent = False

            if flight_should_be_sent:
                flights_to_be_sent.append(flight)

        # Sending info by email about found flights
        if len(flights_to_be_sent) >= 1:
            secret = database_manager.getEmailUnsubscirbeSecretByEmail(entry.email)
            notification_manager.sendFoundFlights(flights_to_be_sent, secret)
            database_manager.insertSentFlights(flights_to_be_sent, entry)


def findFlightsForEntry(entry:FlightEntry) -> [FlightData]:
    if entry.round_trip:
        return flight_search.find_round_trip_flight(fly_from=entry.departure_iata, fly_to=entry.arrival_iata,
                                                             date_from=entry.earliest_departure_date,
                                                             date_to=entry.latest_departure_date,
                                                             price_to=entry.highest_price,
                                                             nights_in_dst_from=entry.shortest_stay,
                                                             nights_in_dst_to=entry.longest_stay)
    else:
        return flight_search.find_one_way_flight(fly_from=entry.departure_iata, fly_to=entry.arrival_iata,
                                                          date_from=entry.earliest_departure_date,
                                                          date_to=entry.latest_departure_date,
                                                          price_to=entry.highest_price)


