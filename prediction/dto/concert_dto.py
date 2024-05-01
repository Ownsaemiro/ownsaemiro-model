class ConcertRequestDto:
    def __init__(self, data):
        self.weekday = data.get('weekday')
        self.region = data.get('region')
        self.genre = data.get('genre')

    def get_concert_data(self):
        return {
            'weekday': self.weekday,
            'region': self.region,
            'genre': self.genre
        }


class ConcertResponseDto:
    def __init__(self, ticket: int):
        self.ticket = ticket

    def get_response(self):
        return {
            'ticket': self.ticket
        }