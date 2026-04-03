from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import os

from backend.password_logic import (
    password_analysis,
    load_passwords,
    build_personal_candidates,
    analyze_personal_candidates,
)

app = FastAPI()

# Allow both local dev and the live Vercel frontend
origins = [
    "http://localhost:5173",
    "http://localhost:4173",
    "https://dolos-nu.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

common_passwords = load_passwords()


class PasswordRequest(BaseModel):
    password: str


class PersonalInfoRequest(BaseModel):
    first_name: Optional[str] = None
    last_name:  Optional[str] = None
    birthdate:  Optional[str] = None
    pet_name:   Optional[str] = None
    city_name:  Optional[str] = None


@app.post("/analyze-password")
def analyze_password(request: PasswordRequest):
    return password_analysis(request.password, common_passwords)


@app.post("/personal-candidates")
def personal_candidates(request: PersonalInfoRequest):
    candidates = build_personal_candidates(
        first_name=request.first_name,
        last_name=request.last_name,
        birthdate=request.birthdate,
        pet_name=request.pet_name,
        city_name=request.city_name,
    )
    results = analyze_personal_candidates(candidates, common_passwords)
    return {"candidates": results}