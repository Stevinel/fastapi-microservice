from django.core.exceptions import ValidationError
from .schemas import *
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from mysite.settings import MAX_PLAYERS_AMOUNT

from callback.models import Game, Player
from callback.utils import get_400_response, get_500_response
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

description = """
We use JWT for auth.
"""

app = FastAPI(
    title="Test Project API",
    description=description,
    version="0.0.1"
)


# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()


# exception handler for auth-jwt
# in production, you can tweak performance using orjson response
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


# provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token to use authorization
# later in endpoint protected
@app.post('/login', tags=['Auth'], responses={200: {"model": LoginMessage}})
def login(user: User, Authorize: AuthJWT = Depends()):
    """
    Use username=test and password=test for now.
    This endpoint will response you with access_token
    to use in header like: "Authorization: Bearer $TOKEN" to get protected endpoints
    """
    if user.username != "test" or user.password != "test":
        raise HTTPException(status_code=401, detail="Bad username or password")

    # subject identifier for who this token is for example id or username from database
    access_token = Authorize.create_access_token(subject=user.username)
    return JSONResponse(status_code=200, content={"access_token": access_token})


# protect endpoint with function jwt_required(), which requires
# a valid access token in the request headers to access.
@app.get('/user', tags=['Auth'], responses={200: {"model": UserMessage}})
def user(Authorize: AuthJWT = Depends()):
    """
    Endpoint response with user that fits "Authorization: Bearer $TOKEN"
    """
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return JSONResponse(status_code=200, content={"user": current_user})


@app.get('/protected_example', tags=['Auth'], responses={200: {"model": UserMessage}})
def protected_example(Authorize: AuthJWT = Depends()):
    """
    Just for test of Auth.

    Auth usage example:
    $ curl http://ip:8000/user

    {"detail":"Missing Authorization Header"}

    $ curl -H "Content-Type: application/json" -X POST \
    -d '{"username":"test","password":"test"}' http://localhost:8000/login

    {"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0IiwiaWF0IjoxNjAzNjkyMjYxLCJuYmYiOjE2MDM2OTIyNjEsImp0aSI6IjZiMjZkZTkwLThhMDYtNDEzMy04MzZiLWI5ODJkZmI3ZjNmZSIsImV4cCI6MTYwMzY5MzE2MSwidHlwZSI6ImFjY2VzcyIsImZyZXNoIjpmYWxzZX0.ro5JMHEVuGOq2YsENkZigSpqMf5cmmgPP8odZfxrzJA"}

    $ export TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0IiwiaWF0IjoxNjAzNjkyMjYxLCJuYmYiOjE2MDM2OTIyNjEsImp0aSI6IjZiMjZkZTkwLThhMDYtNDEzMy04MzZiLWI5ODJkZmI3ZjNmZSIsImV4cCI6MTYwMzY5MzE2MSwidHlwZSI6ImFjY2VzcyIsImZyZXNoIjpmYWxzZX0.ro5JMHEVuGOq2YsENkZigSpqMf5cmmgPP8odZfxrzJA

    $ curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/user

    {"user":"test"}

    $ curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/protected_example

    {"user":"test", "test": true}
    """
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return JSONResponse(status_code=200, content={"user": current_user})


@app.post('/new_player', tags=['Main'], responses={
    200: {"model": StatusMessage},
    400: {"model": ErrorMessage},
    500: {"model": ErrorMessage}
    }
)
def create_new_player(player: PlayerItem, Authorize: AuthJWT = Depends()):
    """
    Creates new player.
    """
    Authorize.jwt_required()

    try:
        new_player = Player()
        new_player.name = player.name
        new_player.email = player.email
        new_player.full_clean()
        new_player.save()
    except ValidationError as e:
        return get_400_response(e.message_dict)
    except Exception as e:
        return get_500_response(e)

    return JSONResponse(content={"status": "success", "id": new_player.id, "success": True})


@app.post('/new_game', tags=['Main'], responses={200: {"model": StatusMessage}, 400: {"model": ErrorMessage}})
def create_new_game(game: GameItem, Authorize: AuthJWT = Depends()):
    """
    Creates new game.
    """
    Authorize.jwt_required()

    new_game = Game()
    new_game.name = game.name
    new_game.save()

    return JSONResponse(content={"status": "success", "id": new_game.id, "success": True})


@app.post('/add_player_to_game', tags=['Main'], responses={200: {"model": StatusMessage}, 400: {"model": ErrorMessage}})
def add_player_to_game(game_id: int, player_id: int, Authorize: AuthJWT = Depends()):
    """
    Adds existing player to existing game.
    """
    Authorize.jwt_required()

    try:
        game = Game.objects.get(id=game_id)
        player = Player.objects.get(id=player_id)
    except (Game.DoesNotExist, Player.DoesNotExist) as e:
        return get_400_response(str(e))

    game_players = game.players.all()

    if game_players.count() == MAX_PLAYERS_AMOUNT:
        return get_400_response(f"The game cannot have more than {MAX_PLAYERS_AMOUNT} players")

    elif player not in game_players:
        game.players.add(player)
        return JSONResponse(content={"status": "success", "id": game_id, "success": True})

    return get_400_response(f"Player with id {player_id} already in game with id {game_id}")

    

