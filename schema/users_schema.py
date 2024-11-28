from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Users(BaseModel):
    id : Optional[int] = None
    username : str
    password : str
    partner_code : str
    token : str

class PartnerCodeRequest(BaseModel):
    partner_code : str  

class ScoreRequest(BaseModel):
    authtoken: str
    phone_no: str    

class LogoutRequest(BaseModel):
    partner_code: str
    username: str    