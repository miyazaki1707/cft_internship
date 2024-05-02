from typing import List, Annotated
from fastapi import FastAPI, Depends, Request, status
from datetime import date, datetime
from passlib.context import CryptContext
from pydantic import BaseModel

from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


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
    {"id": 2, "username": "vladimir0", "hashed_password": "$2b$12$24MtqXLyaRX5U4ASf8uTj.lKHyaIKVcIgZ59ECo5BCRzxdFvWrVzy",
     "salary": 76000, "next_increase": date.fromisoformat('2024-12-01')},
    {"id": 3, "username": "petr_vasilech", "hashed_password": "$2b$12$44PEm/ekd9adkJ01jcKN2ONpEgWOBZx1T9bvgKWKqUvBsH98UX3ie",
     "salary": 120000, "next_increase": date.fromisoformat('2024-06-04')}
]


@app.get("/", response_model=List[User])
def get_users():
    return users


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


@app.post("/pass")
def hash_pass(password: str):
    return hash_password(password)


@app.post("/auth")
def auth(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = [user for user in users if user.get("username") == form_data.username][0]  # try catch user field
    authorized = verify_password(form_data.password, user.get("hashed_password"))
    if authorized:
        redirect_url = request.url_for('data')
        return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    else:
        return {"Incorrect password"}


@app.get("/data")
def data():
    return {"auth complete"}