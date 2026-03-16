from pydantic import BaseModel
from datetime import datetime
class ClientOut(BaseModel):
    name : str | None=None
    email : str | None=None
    phoneNum : str | None=None

class ResponseOut(BaseModel):
    prediction: str
    probability : float
    cliente: ClientOut
    timestamp : datetime