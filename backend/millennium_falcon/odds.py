import sqlite3

from .abstract import Planet, Route

AUTONOMY_KEY = "autonomy"
DEPARTURE_KEY = "departure"
ARRIVAL_KEY = "arrival"
ROUTE_DB_KEY = "routes_db"

COUNTDOWN_KEY = "countdown"
BOUNTY_HUNTERS_KEY = "bounty_hunters"

PLANET_KEY = "planet"
DAY_KEY = "day"

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
            dst = Planet(route[1])
            planets.update({route[1]: dst})
        else:
            dst = planets[route[1]]
        # Add to source planet
        src.establish_route(Route(src, dst, cost))
        # Add to destination planet
        dst.establish_route(Route(dst, src, cost))

    # Clean up
    conn.close()

    return planets

def peep_empire_plan(empire_plan):
    """
    {
        "countdown": 6, 
        "bounty_hunters": [
            {"planet": "Tatooine", "day": 4 },
            {"planet": "Dagobah", "day": 5 }
        ]
    }
    """
    count_down = 0
    bounty_hunter_plan = dict()

    if COUNTDOWN_KEY in empire_plan.keys():
        count_down = empire_plan[COUNTDOWN_KEY]
    if BOUNTY_HUNTERS_KEY in empire_plan.keys():
        for plan in empire_plan[BOUNTY_HUNTERS_KEY]:
            if PLANET_KEY not in plan.keys() or DAY_KEY not in plan.keys():
                # Ignore if information is not complete
                continue
            if plan[PLANET_KEY] in bounty_hunter_plan.keys():
                bounty_hunter_plan[plan[PLANET_KEY]].add(plan[DAY_KEY])
            else:
                days = set()
                days.add(plan[DAY_KEY])
                bounty_hunter_plan.update({ \
                    plan[PLANET_KEY]: days \
                })
    return count_down, bounty_hunter_plan

def calculate(falcon_status, empire_plan):
    error_code = 0
    odds = 0.0

    # Falcon auto-check
    if not falcon_autocheck(falcon_status):
        return 1, odds

    # Falcon data load
    planets = retrieve_falcon_db_data(falcon_status[ROUTE_DB_KEY])

    # Empire plan review
    count_down, bounty_hunter_plan = peep_empire_plan(empire_plan)

    # Find the shortest path
    shortest_path = find_shortest_path(planets, \
        falcon_status[DEPARTURE_KEY], falcon_status[ARRIVAL_KEY])
    if len(shortest_path) == 0:
        # Failed to find a valid path
        return 1, odds
    shortest_path_days = calculate_days(shortest_path, falcon_status[AUTONOMY_KEY])
    print("Shortest path days:", shortest_path_days)
    if shortest_path_days > count_down:
        return 0, 0.0
    # Although calculate_days can handle with the autonomy,
    # fixup with stays (None) for further improvement
    shortest_path = fixup_days(shortest_path, falcon_status[AUTONOMY_KEY])

    # TODO: Solve the minimum

    return error_code, odds

def fixup_days(routes, autonomy):
    current_autonomy = autonomy
    new_routes = []
    for route in routes:
        if route is None:
            current_autonomy = autonomy
            new_routes.append(None)
        else:
            if route.cost > current_autonomy:
                new_routes.append(None)
                current_autonomy = autonomy - route.cost
            else:
                current_autonomy = current_autonomy - route.cost
            new_routes.append(route)
    return new_routes

def calculate_days(routes, autonomy):
    """
    Routes is a list containing the routes, None represents staying at the current
    """
    days = 0
    current_autonomy = autonomy
    for route in routes:
        if route is None:
            days = days + 1
            current_autonomy = autonomy
        else:
            if route.cost > autonomy:
                raise Exception("Cost larger than autonomy")
            if route.cost > current_autonomy:
                days = days + 1 + route.cost
                current_autonomy = autonomy - route.cost
            else:
                days = days + route.cost
                current_autonomy = current_autonomy - route.cost
    return days

import heapq

# Helper for comparing
class PriorityPlanetWrapper:
    def __init__(self, priority, planet):
        self.priority = priority
        self.planet = planet
    
    def __lt__(self, other):
        return self.priority < other.priority


def find_shortest_path(planets, src_name, dst_name):
    if src_name not in planets.keys() or dst_name not in planets.keys():
        # Error
        raise Exception("No such planet")
    # Retrieve planets
    src = planets[src_name]
    dst = planets[dst_name]

    current_queue = []  # Create a priority queue
    heapq.heappush(current_queue, PriorityPlanetWrapper(0, src))

    # Retrieve the shortest path
    precedents = { planet: None for _, planet in planets.items() }
    shortest_routes = [] # Chosen routes

    found_dest = False

    shortest_distances = { planet: \
        (None if planet is not src else 0) for _, planet in planets.items() }
    while len(current_queue) > 0:
        # Retrieve the planet without index
        current_planet = heapq.heappop(current_queue).planet

        if current_planet == dst:
            # We have reached the planet
            found_dest = True
            break

        for current_route in current_planet.routes:
            # Do not process the planets with known routes
            #if current_route.dest in known_shortest_path_planets:
            #    continue

            current_reachable_planet = current_route.dest

            is_infinite = (shortest_distances[current_reachable_planet] is None)
            new_distance = shortest_distances[current_planet] + current_route.cost
            if is_infinite or new_distance < shortest_distances[current_reachable_planet]:
                # Update the current reachable shortest distance
                shortest_distances[current_reachable_planet] = new_distance
                heapq.heappush(current_queue,
                    PriorityPlanetWrapper(new_distance, current_reachable_planet)
                )
                # Build the precursor
                precedents[current_reachable_planet] = current_planet

    if not found_dest:
        # No reachable path
        return shortest_routes

    # Build the routes
    current_planet = dst
    while current_planet is not src and current_planet is not None:
        previous_planet = precedents[current_planet]
        if previous_planet is not None:
            for route in previous_planet.routes:
                if route.source == previous_planet and route.dest == current_planet:
                    shortest_routes.insert(0, route)
                    break
        current_planet = previous_planet
    print("Shortest:", shortest_distances[dst])
    return shortest_routes
