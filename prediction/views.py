from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .apps import PredictionFactory
from .dto.concert_dto import ConcertRequestDto, ConcertResponseDto
from .dto.sports_dto import SportsRequestDto, SportsResponseDto

import logging


@csrf_exempt
def prediction_concert(request):
    request_dto = None

    try:
        data = JSONParser().parse(request)
        request_dto = ConcertRequestDto(data=data)
    except:
        logging.error("Parsing Error")
        return JsonResponse({
            "success": False,
            "data": None,
            "error": {
                "code": 40400,
                "message": "not parsing"
            },
        },
            status=400,
            safe=False
        )

    prediction = PredictionFactory.get_instance()
    ticket = prediction.concert_predict(request_dto.get_concert_data())

    return JsonResponse(
        ConcertResponseDto(
            ticket=ticket
        ).get_response(), safe=False
    )


@csrf_exempt
def prediction_sports(request):
    request_dto = None

    try:
        data = JSONParser().parse(request)
        request_dto = SportsRequestDto(data=data)
    except:
        logging.error("Parsing Error")
        return JsonResponse({
            "success": False,
            "data": None,
            "error": {
                "code": 40400,
                "message": "not parsing"
            },
        },
            status=400,
            safe=False
        )

    prediction = PredictionFactory.get_instance()
    spectator = prediction.sports_predict(request_dto.get_request_data())

    return JsonResponse(
        SportsResponseDto(
            spectator=spectator
        ).get_response(), safe=False
    )

