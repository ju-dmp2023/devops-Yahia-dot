import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from fastapi import HTTPException
import numpy as np

from calculator_helper import CalculatorHelper

from models import Calculation, User, ResultResponse, UserResponse, ErrorResponse

def normal_dist_sleep(mean=2, stddev=1, min_sleep=1, max_sleep=4):
    """
    Sleep for a random time drawn from a normal distribution.

    Args:
        mean (float): Mean value of the normal distribution (default=2).
        stddev (float): Standard deviation of the distribution (default=1).
        min_sleep (float): Minimum allowed sleep duration in seconds (default=1).
        max_sleep (float): Maximum allowed sleep duration in seconds (default=4).

    The function will keep sampling until the generated value falls within
    the allowed range, then sleep for that duration.
    """
    while True:
        # Generate a sleep time from a normal distribution
        sleep_time = np.random.normal(mean, stddev)
        # Check if the sleep time is within the allowed range
        if min_sleep <= sleep_time <= max_sleep:
            break  # If it's within the range, proceed

    # Sleep for the computed duration
    time.sleep(sleep_time)

# init FastAPI app
app = FastAPI(title='Calculator', docs_url='/', description="Calculator API", version='1.0.0')

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# defining exceptional JSON-response
@app.exception_handler(Exception)
async def error_handler(request, exc):
    """
    Global exception handler for the API.

    Args:
        request: The HTTP request that caused the exception.
        exc (Exception): The raised exception.

    Returns:
        JSONResponse: A JSON response containing the error detail.
    """
    return JSONResponse({
        'detail': f'{exc}'
    })

@app.post('/calculate', operation_id='calculate', summary='Basic arithmetic calculation', response_model=ResultResponse, tags=["actions"], responses={500: {"model": ErrorResponse}})
async def calc(body: Calculation):
    """
    Perform a basic arithmetic calculation.

    Args:
        body (Calculation): The request body containing operands and operation.

    Returns:
        ResultResponse: The result of the calculation.

    Raises:
        HTTPException: 500 if the calculation fails.
    """
    try:
        result = body.calculate()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/register', operation_id='register', summary='Register new user', response_model=UserResponse, tags=["actions"], responses={409: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def register(body: User):
    """
    Register a new user.

    Args:
        body (User): The request body containing user credentials.

    Returns:
        UserResponse: The registered user details.

    Raises:
        HTTPException:
            409 if the user already exists.
            500 if registration fails.
    """
    try:
        result = body.register()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if result is None:
        raise HTTPException(status_code=409, detail='User already exists.')
    return result


@app.post('/login', operation_id='login', summary='Login a user', response_model=UserResponse, tags=["actions"], responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def login(body: User):
    """
    Log in a user.

    Args:
        body (User): The request body containing login credentials.

    Returns:
        UserResponse: The logged-in user details.

    Raises:
        HTTPException:
            400 if credentials are invalid.
            500 if login fails.
    """
    try:
        result = body.login()
        normal_dist_sleep()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if result is None:
        raise HTTPException(status_code=400, detail='Wrong username of password.')
    return result

@app.get('/users/current', operation_id='users_current', summary='Get current logged in user', response_model=UserResponse, tags=["actions"], responses={204: {"model": None}, 500: {"model": ErrorResponse}})
async def users_current():
    """
    Get the currently logged-in user.

    Returns:
        UserResponse: The current user's details.

    Raises:
        HTTPException:
            204 if no user is logged in.
            500 if retrieval fails.
    """
    def current_user():
        user = CalculatorHelper().get_current_user()
        if user is not None:
            response = UserResponse()
            response.username = user.username
            return response
        return None

    try:
        result = current_user()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if result is None:
        raise HTTPException(status_code=204, detail='No user has signed in.')
    return result


@app.post('/logout', operation_id='logout', summary='Logout current user', response_model=UserResponse, tags=["actions"], responses={500: {"model": ErrorResponse}})
async def logout():
    """
    Log out the current user.

    Returns:
        UserResponse: The logged-out user's details.

    Raises:
        HTTPException:
            204 if no user is logged in.
            500 if logout fails.
    """
    def logout():
        user = CalculatorHelper().logout()
        if user is not None:
            response = UserResponse()
            response.username = user.username
            return response
        return None

    try:
        result = logout()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if result is None:
        raise HTTPException(status_code=204, detail='No user has signed in.')
    return result

def main(args):
    """
    Entry point for running the Calculator API with uvicorn.

    Args:
        args (list[str]): Command-line arguments.

    The function parses CLI arguments, sets default values from environment
    variables if present, and starts the uvicorn server on 0.0.0.0.
    """
    import os
    import uvicorn
    import argparse

    def ifenv(key, default):
        """
        Helper to use environment variable as default value if present.

        Args:
            key (str): Environment variable key.
            default (str): Default value.

        Returns:
            dict: Dictionary with 'default' key for argparse.
        """
        return (
            {'default': os.environ.get(key)} if os.environ.get(key)
            else {'default': default}
        )

    parser = argparse.ArgumentParser(description='Calculator server')

    parser.add_argument('--port', type=int, default='5000', help='Port, 5000 is default')
    parser.add_argument("--loglevel", **ifenv('LOGLEVEL', 'DEBUG'), choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help="Set Flask logging level, DEBUG is default")
    parser.add_argument('--debug', action='store_true', help='Flask debug')
    parser.add_argument('--no-debug', dest='debug', action='store_false', help='Flask no debug is default')
    parser.add_argument('-r', '--rest', action='store_true')
    parser.set_defaults(debug=True)

    args = parser.parse_args()

    # Listen on all network interfaces
    #app.run('0.0.0.0', port=args.flask_port, debug=args.debug)
    uvicorn.run(app, host="0.0.0.0", port=args.port)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

