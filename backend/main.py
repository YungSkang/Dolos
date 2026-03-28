from fastapi import FastAPI
from pydantic import BaseModel

from backend.password_logic import password_analysis, load_passwords

app = FastAPI()

# load passwords at startup
common_passwords = load_passwords()


# request password
class PasswordRequest(BaseModel):
    password: str


# create endpoint
@app.post("/analyze-password")
def analyze_password(request: PasswordRequest):
    password = request.password

    result = password_analysis(password, common_passwords)

    return result