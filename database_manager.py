import datetime
import random
import mysql.connector
from flight_entry import FlightEntry
from sent_flight import SentFlight
from email_unsubscribe_secret import EmailUnsubscribeSecret
from flight_data import FlightData
import config

cnx: mysql.connector.CMySQLConnection
cur: mysql.connector.connection_cext.CMySQLCursor

def connectToDatabase() -> bool:
    '''Returns True if connection was successful'''
    global cnx
    global cur
    cnx = mysql.connector.connect(host=config.DB_HOST , user=config.DB_USER, password=config.DB_PASSWORD, database=config.DB)
    if cnx.is_connected():
        cur = cnx.cursor(buffered=True)
        return True
    else:
        return False


def discconectFromDatabase():
    cnx.close()


def getAllFlightEntries() -> [FlightEntry]:
    query = ("SELECT email, departure_iata, arrival_iata, earliest_departure_date, latest_departure_date, round_trip, "
             "shortest_stay, longest_stay, highest_price, id, created_at FROM flight_entries")
    cur.execute(query)

    all_entries = []
    for (email, departure_iata, arrival_iata, earliest_departure_date, latest_departure_date, round_trip,
         shortest_stay, longest_stay, highest_price, id, created_at) in cur:
        entry = FlightEntry(email, departure_iata, arrival_iata, earliest_departure_date,
                                         latest_departure_date, round_trip, shortest_stay, longest_stay,
                                         highest_price, id=id, created_at=created_at)
        all_entries.append(entry)

    return all_entries


def getAllSentFlights() -> [SentFlight]:
    query = ("SELECT id, created_at, flight_entry_id, price, departure_date FROM sent_flights")
    cur.execute(query)

    all_sent_flights = []
    for (id, created_at, flight_entry_id, price, departure_date) in cur:
        sent = SentFlight(id, created_at, flight_entry_id, price, departure_date)
        all_sent_flights.append(sent)

    return all_sent_flights


def getAllEmailUnsubscribeSecrets() -> [EmailUnsubscribeSecret]:
    query = ("SELECT email, unsubscribe_secret FROM email_unsubscribe_secrets")
    cur.execute(query)

    all_email_secrets = []
    for (email, unsubscribe_secret) in cur:
        email_secrete = EmailUnsubscribeSecret(email, unsubscribe_secret)
        all_email_secrets.append(email_secrete)

    return all_email_secrets


def getAllSentFlightsWithEntryId(entry_id) -> [SentFlight]:
    query = (f"SELECT id, created_at, flight_entry_id, price, departure_date FROM sent_flights "
             f"WHERE flight_entry_id = {entry_id}")
    cur.execute(query)

    all_sent_flights = []
    for (id, created_at, flight_entry_id, price, departure_date) in cur:
        sent = SentFlight(id, created_at, flight_entry_id, price, departure_date)
        all_sent_flights.append(sent)

    return all_sent_flights


def getEmailUnsubscirbeSecretByEmail(email:str) -> EmailUnsubscribeSecret:
    query = (f"SELECT email, unsubscribe_secret FROM email_unsubscribe_secrets WHERE email = '{email}'")
    cur.execute(query)

    for (email, unsubscribe_secret) in cur:
        return EmailUnsubscribeSecret(email, unsubscribe_secret)



# SQL INJECTION DANGER!!!!!!!!!!!!
def insertFlightEntry(entry: FlightEntry):
    MAX_SECRET_VALUE = 30000
    query = (f"INSERT INTO flight_entries"
             f"(email, departure_iata, arrival_iata, earliest_departure_date, latest_departure_date, round_trip, "
             f"shortest_stay, longest_stay, highest_price) VALUES "
             f"('{entry.email}', '{entry.departure_iata}', '{entry.arrival_iata}', '{entry.earliest_departure_date}', "
             f"'{entry.latest_departure_date}', {entry.round_trip}, {entry.shortest_stay}, {entry.longest_stay}, "
             f"{entry.highest_price})")
    query = query.replace("None", "NULL")
    cur.execute(query)

    # Insert email to unsubscribe_secrets if email is not already there
    query = (f"SELECT COUNT(*) AS amount FROM email_unsubscribe_secrets WHERE email='{entry.email}'")
    cur.execute(query)
    for amount in cur.fetchall():
        if amount[0] == 0:
            secret = random.randint(0, MAX_SECRET_VALUE)
            query = (f"INSERT INTO email_unsubscribe_secrets(email, unsubscribe_secret) VALUES ('{entry.email}', {secret})")
            cur.execute(query)

    cnx.commit()


def insertSentFlights(sent_flights:list[FlightData], entry: FlightEntry):
    query = (f"INSERT INTO sent_flights"
             f"(flight_entry_id, price, departure_date) VALUES ")
    for index in range(len(sent_flights)):
        departure_date = datetime.datetime.strptime(sent_flights[index].local_departure.split('T')[0], '%Y-%m-%d')
        query += f"({entry.id}, {sent_flights[index].price_eur}, '{departure_date}')"
        # If this is not the last flight, then add coma
        if index < len(sent_flights) - 1:
            query += ", "
    query = query.replace("None", "NULL")
    cur.execute(query)

    cnx.commit()


def deleteOldEntry(entry: FlightEntry):
    query = (f"DELETE FROM sent_flights WHERE flight_entry_id = {entry.id}")
    cur.execute(query)
    query = (f"DELETE FROM flight_entries WHERE id = {entry.id}")
    cur.execute(query)

    cnx.commit()


def emailAndSecretMatch(email: str, secret:int) -> bool:
    query = (f"SELECT email, unsubscribe_secret FROM email_unsubscribe_secrets WHERE email = '{email}'")
    cur.execute(query)

    all_secrets = []
    for (email, unsubscribe_secret) in cur:
        all_secrets.append(unsubscribe_secret)

    if len(all_secrets) == 0:
        return False
    elif len(all_secrets) == 1:
        return secret == all_secrets[0]
    else:
        raise Exception("Found more than one unsubscribe secret for one email. This can not happen.")
        return False


def deleteAllDataWithEmail(email: str):
    query = (f"DELETE FROM sent_flights WHERE flight_entry_id IN (SELECT id FROM flight_entries WHERE email = '{email}')")
    cur.execute(query)
    query = (f"DELETE FROM flight_entries WHERE email = '{email}'")
    cur.execute(query)

    cnx.commit()


