from typing import List, Annotated
from fastapi import FastAPI, Depends, Request, status, HTTPException, Response
from datetime import date, datetime
from passlib.context import CryptContext
from pydantic import BaseModel

import jwt
import time

from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

TOKEN_EXPIRES_TIME = 5
SECRET = "45hgrt31df241k3uk4a31gs1jh2q4r53aw1f31jktu23i41e31fa3"
ALGORITHM = "HS256"

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    id: int
    username: str
    hashed_password: str
    salary: int
    next_increase: datetime


users = [
    {"id": 1, "username": "soramiyazaki",
     "hashed_password": "$2b$12$g0LK.zKxgmnJ/O8UeMroLu/dzoaMhEXZoXH/TUXmzl1NSmJGtTgCm",
     "salary": 60000, "next_increase": date.fromisoformat('2024-08-15')},
    {"id": 2, "username": "vladimir0",
     "hashed_password": "$2b$12$24MtqXLyaRX5U4ASf8uTj.lKHyaIKVcIgZ59ECo5BCRzxdFvWrVzy",
     "salary": 76000, "next_increase": date.fromisoformat('2024-12-01')},
    {"id": 3, "username": "petr_vasilech",
     "hashed_password": "$2b$12$44PEm/ekd9adkJ01jcKN2ONpEgWOBZx1T9bvgKWKqUvBsH98UX3ie",
     "salary": 120000, "next_increase": date.fromisoformat('2024-06-04')}
]


@app.post("/login")
def login(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user = [user for user in users if user.get("username") == form_data.username][0]
        authorized = verify_password(form_data.password, user.get("hashed_password"))
        if authorized:
            token = create_jwt(user.get("username"))
            redirect_url = request.url_for('get_user_data')
            response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
            response.set_cookie(key="Authorization", value=token)
            return response
        else:
            return {"Incorrect password"}
    except:
        return {"Incorrect username"}


@app.get("/data")
def get_user_data(request: Request):
    token = request.cookies.get("Authorization")
    try:
        decoded_token = decode_jwt(token)
        if decoded_token is None:
            raise HTTPException(status_code=401)
        user = [user for user in users if user.get("username") == decoded_token.get("username")][0]
        return {
            "salary": user.get("salary"),
            "Next Increase": user.get("next_increase")
        }
    except:
        raise HTTPException(status_code=401)


def create_jwt(username: str):
    payload = {
        "username": username,
        "expires": time.time() + 30
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return token


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        raise HTTPException(status_code=401)  # write an exception


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)
