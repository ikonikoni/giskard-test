import sqlite3

AUTONOMY_KEY = "autonomy"
DEPARTURE_KEY = "departure"
ARRIVAL_KEY = "arrival"
ROUTE_DB_KEY = "routes_db"

def falcon_autocheck(falcon_status):
    """
        Check the key-values in falcon status:
        {
            "autonomy": 6,
            "departure": "Tatooine",
            "arrival": "Endor",
            "routes_db": "universe.db"
        }
    """
    falcon_status_keys = falcon_status.keys()

    if AUTONOMY_KEY not in falcon_status_keys:
        return False

    if DEPARTURE_KEY not in falcon_status_keys:
        return False

    if ARRIVAL_KEY not in falcon_status_keys:
        return False

    if ROUTE_DB_KEY not in falcon_status_keys:
        return False

    return True

def retrieve_falcon_db_data(falcon_planet_db_fn):
    # Check if the db exists
    # TODO: Check if the table exists
    pass

def calculate(falcon_status, empire_plan):
    error_code = 0
    odds = 0.0

    # Falcon auto-check
    if not falcon_autocheck(falcon_status):
        return 1, odds

    # Falcon data load
    map = retrieve_falcon_db_data(falcon_status[ROUTE_DB_KEY])

    # TODO: Empire plan review

    return error_code, odds
