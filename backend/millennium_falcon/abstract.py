
class Planet:
    # Vertex
    def __init__(self, name):
        self._name = name
        self._routes = set()
    
    def establish_route(self, route):
        self._routes.add(route)
    
    @property
    def routes(self):
        return self._routes
    
    @property
    def name(self):
        return self._name

class Route:
    # Edge
    def __init__(self, src, dst, cost):
        self._src = src
        self._dst = dst
        self._cost = cost
    
    @property
    def cost(self):
        return self._cost
    
    @property
    def source(self):
        return self._src
    
    @property
    def dest(self):
        return self._dest
