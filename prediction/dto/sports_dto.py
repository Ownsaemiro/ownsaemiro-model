class SportsRequestDto:
    def __init__(self, data):
        self.organization = data.get('organization')
        self.weekday = data.get('weekday')
        self.home = data.get('home')
        self.away = data.get('away')
        self.weather = data.get('weather')
        self.degree = data.get('degree')
        self.region = data.get('region')

    def get_request_data(self):
        return {
            'organization': self.organization,
            'weekday': self.weekday,
            'home': self.home,
            'away': self.away,
            'weather': self.weather,
            'degree': self.degree,
            'region': self.region
        }
    

class SportsResponseDto:
    def __init__(self, spectator: int):
        self.spectator = spectator

    def get_response(self):
        return {
            'spectator': self.spectator
        }