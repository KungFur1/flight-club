CREATE DATABASE flight_club;

USE flight_club;

CREATE TABLE flight_entries
(
	id INT PRIMARY KEY AUTO_INCREMENT,
    created_at DATETIME NOT NULL DEFAULT NOW(),
    email VARCHAR(255) NOT NULL,
    departure_iata CHAR(3) NOT NULL,
    arrival_iata CHAR(3) NOT NULL,
    earliest_departure_date DATE NOT NULL,
    latest_departure_date DATE NOT NULL,
    round_trip BOOL NOT NULL,
		shortest_stay INT UNSIGNED,
        longest_stay INT UNSIGNED,
	highest_price INT UNSIGNED NOT NULL,
    CONSTRAINT if_round_trip_is_true_then_stay_is_not_null CHECK(NOT round_trip OR (longest_stay IS NOT NULL AND shortest_stay IS NOT NULL))
    -- SHOULD ADD MORE CHECKS
);


CREATE TABLE sent_flights
(
	id INT PRIMARY KEY AUTO_INCREMENT,
    created_at DATETIME NOT NULL DEFAULT NOW(),
    flight_entry_id INT,
    FOREIGN KEY (flight_entry_id) REFERENCES flight_entries(id),
    price DOUBLE NOT NULL,
    departure_date DATE NOT NULL
);


CREATE TABLE email_unsubscribe_secrets
(
	email VARCHAR(255) PRIMARY KEY,
    unsubscribe_secret INT UNSIGNED NOT NULL
);

DROP DATABASE flight_club;
DROP TABLE sent_flights;

SELECT * FROM flight_entries;

