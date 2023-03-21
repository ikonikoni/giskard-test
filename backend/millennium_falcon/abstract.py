
class Planet:
    # Vertex
    def __init__(self, name):
        self._name = name
        self._routes = set()
    
    def establish_route(self, route):
        self._routes.add(route)

class Route:
    # Edge
    def __init__(self, src, dst, cost):
        self._src = src
        self._dst = dst
        self._cost = cost
