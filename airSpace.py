from navAirpoint import *
from navSegment import *

class AirSpace:
    def __init__(self):
        self.nav_points = []
        self.nav_airports = []
        self.nav_segments = []
        self.is_real_map = False  # Flag to identify real maps

    def load_real_map(self, region):
        self.is_real_map = True
        standard_regions = {'Catalunya': 'Cat', 'España': 'Spain', 'Europa': 'ECAC'}

        if region not in standard_regions:
            raise ValueError(f"Unknown region: {region}")

        prefix = standard_regions[region]
        self.loaded_prefix = prefix  # Store the prefix used to load this map

        # Rest of the loading code remains the same...
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

        # Load airports
        with open(f'{prefix}_aer.txt', 'r') as f:
            for line in f:
                name = line.strip()
                if name:
                    self.nav_airports.append(name)

        # Load segments
        with open(f'{prefix}_seg.txt', 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 3:
                    self.nav_segments.append({
                        'origin_id': parts[0],
                        'dest_id': parts[1],
                        'distance': float(parts[2])
                    })
        return self

def is_real_map(graph):
    return hasattr(graph, 'is_real_map') and graph.is_real_map
