from typing import List
from fastapi import FastAPI
from datetime import date, datetime

from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    username: str
    hashed_password: str
    salary: int
    next_increase: datetime

users = [
    {"id": 1, "username": "soramiyazaki", "hashed_password": "vasd7829jnasda09182903kjsndla901", 
     "salary": 60000, "next_increase": date.fromisoformat('2024-08-15')},
     {"id": 2, "username": "lit", "hashed_password": "1231a7829jnasadadda09182903kjsndla901", 
     "salary": 76000, "next_increase": date.fromisoformat('2024-12-01')},
     {"id": 3, "username": "petr_vasilech", "hashed_password": "1293asdasjdlakdAalkLKSA", 
     "salary": 120000, "next_increase": date.fromisoformat('2024-06-04')}
]


@app.get("/", response_model=List[User])
def get_users():
    return users