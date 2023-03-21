import sqlite3

from .abstract import Planet, Route

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
    # Assume the db exists
    conn = sqlite3.connect(falcon_planet_db_fn)

    # Try to directly retrieve the data
    planets = dict()
    for route in conn.execute("select * from `ROUTES`"):
        print(route)
        src = None
        dst = None
        cost = route[2]

        if route[0] not in planets.keys():
            # Create a new planet
            src = Planet(route[0])
            planets.update({route[0]: src})
        else:
            src = planets[route[0]]

        if route[1] not in planets.keys():
            # Create a new planet
            src = Planet(route[1])
            planets.update({route[1]: src})
        else:
            dst = planets[route[1]]
        # Add to source planet
        src.establish_route(Route(src, dst, cost))
        # Add to destination planet
        src.establish_route(Route(dst, src, cost))

    # Clean up
    conn.close()

    return planets

def calculate(falcon_status, empire_plan):
    error_code = 0
    odds = 0.0

    # Falcon auto-check
    if not falcon_autocheck(falcon_status):
        return 1, odds

    # Falcon data load
    planets = retrieve_falcon_db_data(falcon_status[ROUTE_DB_KEY])

    # TODO: Empire plan review

    return error_code, odds
