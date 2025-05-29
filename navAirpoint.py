class NavAirport:
    '''Definimos la clase NavAirport, que son los aeropuertos del gráfico'''

    def __init__(self, name: str):
        self.name = name
        self.sids = []  # Waypoints para despegues (D)
        self.stars = []  # Waypoints para llegadas (A)
        self.other = []  # Waypoints que pueden ser ambos

    def add_waypoint(self, waypoint_name: str):
        """Clasifica los puntos según la última letra"""
        if waypoint_name.endswith('D'):
            self.sids.append(waypoint_name)
        elif waypoint_name.endswith('A'):
            self.stars.append(waypoint_name)
        else:
            self.other.append(waypoint_name)

    def get_departure_points(self):
        """Devuelve todos los puntos válidos de despegue (SIDs + other)"""
        return self.sids + self.other

    def get_arrival_points(self):
        """Deuelve todos los puntos válidos de aterrizaje (STARs + other)"""
        return self.stars + self.other