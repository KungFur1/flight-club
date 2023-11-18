# app
DEV_MODE = False
BASE_URL = "https://flightclub-378407.lm.r.appspot.com"

# Tequila API
TEQUILA_API_KEY = READ_FROM_ENVIRONMENT
TEQUILA_AUTHORIZATION_HEADER = {
    "apikey": TEQUILA_API_KEY
}
TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
TEQUILA_LOCATIONS_ENDPOINT = TEQUILA_ENDPOINT + "/locations/query"
TEQUILA_SEARCH_ENDPOINT = TEQUILA_ENDPOINT + "/v2/search"

# Database
DB_HOST = '34.116.180.230'
DB_USER = 'root'
DB_PASSWORD = READ_FROM_ENVIRONMENT
DB = 'flight_club'
