from navAirpoint import *
from navSegment import *


class AirSpace:
    def __init__(self):
        self.nav_points = []
        self.nav_airports = []
        self.nav_segments = []
        self.is_real_map = False
        self.airport_data = {}

    def load_real_map(self, region):
        '''Prepara el mapa real que queremos importar'''
        self.is_real_map = True
        standard_regions = {'Catalunya': 'Cat', 'España': 'Spain', 'Europa': 'ECAC'}
        if region not in standard_regions:
            raise ValueError(f"Unknown region: {region}")
        prefix = standard_regions[region]
        with open(f'{prefix}_nav.txt', 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 4:
                    self.nav_points.append({
                        'id': parts[0],
                        'name': parts[1],
                        'lat': float(parts[2]),
                        'lon': float(parts[3])
                    })
        with open(f'{prefix}_aer.txt', 'r') as f:
            for line in f:
                name = line.strip()
                if name:
                    self.nav_airports.append(name)
                    self.airport_data[name] = NavAirport(name)
        with open(f'{prefix}_seg.txt', 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 3:
                    self.nav_segments.append({
                        'origin_id': parts[0],
                        'dest_id': parts[1],
                        'distance': float(parts[2])
                    })
        for point in self.nav_points:
            point_name = point['name']
            for airport in self.nav_airports:
                if point_name.startswith(airport):
                    self.airport_data[airport].add_waypoint(point_name)
        return self

def is_real_map(graph):
    '''Aclara si estamos usando un mapa real o uno inventado'''
    return hasattr(graph, 'is_real_map') and graph.is_real_map
