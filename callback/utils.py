from django.core.validators import RegexValidator
# from .models import Game, Player

from fastapi.responses import JSONResponse


def name_regex():
    """
    Player model name validator
    """
    name_regex = RegexValidator(
        regex="[A-Fa-f0-9]+",
        message="The name must contain only numbers from 0-9 and only letters from a-f")
    return name_regex


def get_400_response(message):
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "message": message
        }
    )


def get_500_response(message):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": message
        }
    )
