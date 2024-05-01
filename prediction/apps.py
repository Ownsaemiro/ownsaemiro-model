from django.apps import AppConfig

import warnings
import joblib
import logging
import pandas as pd

warnings.filterwarnings("ignore", category=FutureWarning)


class PredictionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prediction'

    def ready(self) -> None:
        PredictionFactory().initialize(
            concert_regressor_path='model/regressor/concert_regressor.joblib',
            concert_encoder_path='model/transformer/concert_transformer.joblib',
            baseball_regressor_path='model/regressor/sports_KBO.joblib',
            baseball_encoder_path='model/transformer/KBO_transformer.joblib',
            soccer_regressor_path='model/regressor/sports_KLEAGUE.joblib',
            soccer_encoder_path='model/transformer/KLEAGUE_transformer.joblib',
        )


class PredictionFactory:
    _instance = None

    @classmethod
    def initialize(cls, **kwargs):
        if cls._instance is None:
            cls._instance = Prediction(**kwargs)
        return cls._instance
    
    @classmethod
    def get_instance(cls):
        return cls._instance


class Prediction:
    def __init__(
            self,
            concert_regressor_path: str,
            concert_encoder_path: str,
            baseball_regressor_path: str,
            baseball_encoder_path: str,
            soccer_regressor_path: str,
            soccer_encoder_path: str
    ):
        self.concert_regressor = joblib.load(concert_regressor_path)
        self.concert_encoder = joblib.load(concert_encoder_path)
        self.baseball_regressor = joblib.load(baseball_regressor_path)
        self.baseball_encoder = joblib.load(baseball_encoder_path)
        self.soccer_regressor = joblib.load(soccer_regressor_path)
        self.soccer_encoder = joblib.load(soccer_encoder_path)
        self.concert_column = [
            'weekday', 'region', 'genre'
        ]
        self.sports_column = [
            'weekday', 'home', 'away', 'region', 'weather', 'degree'
        ]

    def concert_predict(self, request: dict) -> int:
        values = [request.get(column_name, None) for column_name in self.concert_column]
        data = pd.DataFrame([values], columns=self.concert_column)

        encoded_data = self.concert_encoder.transform(data)
        predicted_data = self.concert_regressor.predict(encoded_data)

        logging.debug(f'Predicted concert ticket is {predicted_data[0]}')
        return int(predicted_data[0])

    def sports_predict(self, request: dict) -> int:
        organization = request.get('organization', None)
        values = [request.get(column_name, None) for column_name in self.sports_column]

        data = pd.DataFrame([values], columns=self.sports_column)

        if organization == 'KBO':
            encoded_data = self.baseball_encoder.transform(data)
            predicted_data = self.baseball_regressor.predict(encoded_data)
        elif organization == 'KLEAGUE':
            encoded_data = self.soccer_encoder.transform(data)
            predicted_data = self.soccer_regressor.predict(encoded_data)
        else:
            predicted_data = [0]

        logging.debug(f'Predicted sports spectator is {predicted_data[0]}')
        return int(predicted_data[0])

