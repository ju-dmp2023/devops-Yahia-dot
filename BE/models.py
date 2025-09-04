from fastapi import Query
from pydantic import BaseModel
from calculator_helper import CalculatorHelper
from enum import Enum

class ErrorResponse(BaseModel):
    detail: str
class Opertions(str, Enum):
    add = "add"
    subtract = "subtract"
    multiply = "multiply"
    divide = "divide"

class Calculation(BaseModel):
    operation: Opertions
    operand1: float
    operand2: float

    def calculate(self):
        calc = CalculatorHelper()
        do = {
                Opertions.add:calc.add,
                Opertions.subtract:calc.subtract,
                Opertions.multiply:calc.multiply,
                Opertions.divide:calc.divide
        }
        result = do[self.operation](self.operand1, self.operand2)
        response = ResultResponse()
        response.result = result
        return response

class User(BaseModel):
    username: str
    password: str

    def register(self):
        username = CalculatorHelper().register_user(self.username, self.password)
        if username is not None:
            response = UserResponse()
            response.username = username
        else:
            response = None
        return response

    def login(self):
        username = CalculatorHelper().login(self.username, self.password)
        if username is not None:
            response = UserResponse()
            response.username = username
        else:
            response = None
        return response

class ResultResponse(BaseModel):
    result: float = None

class UserResponse(BaseModel):
    username: str = None


