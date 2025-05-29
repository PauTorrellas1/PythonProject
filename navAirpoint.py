class NavAirport:
    '''Definimos la clase NavAirport, que son los aeropuertos del gráfico'''
    def __init__(self, name: str):
        self.name = name
        self.sids = []
        self.stars = []