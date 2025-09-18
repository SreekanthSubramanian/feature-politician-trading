from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta
from pydantic import BaseModel
import requests
import json

#config
SECRET_KEY = "supersecretkey123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# simple userdb
users_db = {
    "demo": {
        "username": "demo",
        "password": "demo1234",  
    }
}

API_KEY = ""
BASE_URL = "https://financialmodelingprep.com/stable"

app = FastAPI()


# creating token for auth
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username not in users_db:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# api
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or form_data.password != user["password"]:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/senate")
async def senate_disclosures(limit: int = 5, user: str = Depends(get_current_user)):
    url = f"{BASE_URL}/senate-latest"
    params = {"limit": limit, "apikey": API_KEY}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


@app.get("/house")
async def house_disclosures(limit: int = 5, user: str = Depends(get_current_user)):
    url = f"{BASE_URL}/house-latest"
    params = {"limit": limit, "apikey": API_KEY}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
