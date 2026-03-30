from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from backend.password_logic import password_analysis, load_passwords

app = FastAPI()
#add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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